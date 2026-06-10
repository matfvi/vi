# TensorFlow Tiny GPT, Explained Step by Step

This script builds a miniature character-level GPT: it turns text into numbers, trains a causal Transformer to predict the next character, and then generates new text one character at a time.

The whole program rests on three ideas:

1. **Characters become token ids.** Neural networks operate on numbers, so every character in the corpus receives a stable integer id.
2. **Training examples are shifted text windows.** The input is a short sequence, and the target is the same sequence shifted one character into the future.
3. **Causal attention blocks the future.** At position `t`, the model may use characters at positions `0..t`, but not positions after `t`.

Think of the model as a student learning to continue a sentence from a tiny flashcard deck. The deck is so small that the student will not become a fluent writer, but the mechanics are the same mechanics used by larger causal language models.

## The Big Picture

The script answers one question: **given the characters seen so far, what character should come next?**

It does that in this order:

1. Build a small vocabulary from the text.
2. Convert the full text into integer token ids.
3. Randomly sample input and target batches from the token ids.
4. Build a causal self-attention layer.
5. Stack attention and feed-forward layers into a tiny Transformer.
6. Train the model with next-character cross-entropy loss.
7. Generate text by repeatedly sampling the next character.

The model is "GPT-like" because it is decoder-only, causal, autoregressive, and predicts the next token from previous tokens.

## 1. Imports

The imports provide the numerical and neural-network tools.

```python
import tensorflow as tf
import numpy as np
```

`numpy` handles simple array operations outside the model, such as encoding text and sampling random batch positions. `tensorflow` builds and trains the neural network.

Metaphor: NumPy is the notebook where we prepare the lesson materials; TensorFlow is the training gym where the model practices.

## 2. Tiny Corpus

The corpus is the entire textbook for this tiny model.

```python
text = """
hello world this is a tiny dataset for a minimal gpt model
we will train a character level transformer on this text only
"""
```

The model does not know English. It only sees this string. Every pattern it learns must come from these characters: letters, spaces, and newline characters.

Because the text is inside triple quotes, it includes newline characters. Those newline characters are real training data, just like `h`, `e`, or a space.

### Vocabulary

The vocabulary is the set of unique characters the model can read and write.

```python
chars = sorted(list(set(text)))
vocab_size = len(chars)
```

`set(text)` removes duplicates. `sorted(...)` gives a deterministic order. `vocab_size` is the number of distinct characters.

For example, if the corpus were:

```text
banana
```

the unique sorted characters would be:

```python
['a', 'b', 'n']
```

and `vocab_size` would be `3`.

Metaphor: the vocabulary is the model's alphabet tray. If a character is not in the tray, the model cannot represent it.

### Character-to-id and id-to-character maps

The two dictionaries let the script move between text and numbers.

```python
stoi = {c:i for i,c in enumerate(chars)}
itos = {i:c for c,i in stoi.items()}
```

`stoi` means "string to integer." It maps each character to its token id.

`itos` means "integer to string." It maps each token id back to its character.

Example:

```python
chars = ['a', 'b', 'n']
stoi = {'a': 0, 'b': 1, 'n': 2}
itos = {0: 'a', 1: 'b', 2: 'n'}
```

Metaphor: `stoi` is the class roster that assigns every student a number. `itos` is the reverse lookup sheet that turns a number back into a name.

### Encoding and decoding

The model cannot train on raw characters, so `encode` turns a string into token ids.

```python
def encode(s): return np.array([stoi[c] for c in s], dtype=np.int32)
```

If `stoi = {'a': 0, 'b': 1, 'n': 2}`, then:

```python
encode("banana")
```

returns:

```python
np.array([1, 0, 2, 0, 2, 0], dtype=np.int32)
```

`decode` reverses the process.

```python
def decode(l): return ''.join([itos[i] for i in l])
```

If `l = [1, 0, 2, 0, 2, 0]`, then:

```python
decode(l)
```

returns:

```text
banana
```

Finally, the whole corpus becomes a numerical array:

```python
data = encode(text)
```

At this point, the training text is no longer a string. It is a one-dimensional array of integer token ids.

## 3. Batch Generator

The batch generator creates practice problems for the model.

```python
block_size = 32
batch_size = 16
```

`block_size` is the context length. Each training example contains `32` characters of input.

`batch_size` is the number of examples processed together. Each batch contains `16` independent text windows.

So each input batch has shape:

```text
(batch_size, block_size) = (16, 32)
```

### Random window starts

The function begins by choosing random starting positions in the encoded corpus.

```python
ix = np.random.randint(0, len(data) - block_size - 1, size=batch_size)
```

This produces `16` random integers. Each integer is a starting index for one training window.

The upper limit is conservative: because `np.random.randint` excludes the high endpoint, this expression leaves the final possible window unused. That is harmless here because the corpus is tiny and the purpose is to demonstrate the method.

Metaphor: imagine cutting 16 short strips from a long paper tape of text. Each strip begins at a random character.

### Inputs and targets

The input batch `x` contains the current characters.

```python
x = np.stack([data[i:i+block_size] for i in ix])
```

The target batch `y` contains the next characters.

```python
y = np.stack([data[i+1:i+block_size+1] for i in ix])
```

Each target is shifted one position to the right.

Example with `block_size = 5`:

```text
text window: hello world

x: h e l l o
y: e l l o _
```

The underscore represents a space. The first input character `h` asks the model to predict `e`. The sequence `h e` asks the model to predict `l`. The sequence `h e l l` asks the model to predict `o`.

That is the central training contract:

```text
At every position, predict the next character.
```

The function returns the pair:

```python
return x, y
```

Both arrays have shape:

```text
(16, 32)
```

### TensorFlow dataset

The `dataset` function wraps the batch generator in a TensorFlow input pipeline.

```python
def dataset():
    def gen():
        while True:
            x, y = get_batch()
            yield x, y
```

`gen` is an infinite generator. Every time TensorFlow asks for data, it creates a new random batch.

The generator is converted to a `tf.data.Dataset`:

```python
return tf.data.Dataset.from_generator(
    gen,
    output_signature=(
        tf.TensorSpec(shape=(batch_size, block_size), dtype=tf.int32),
        tf.TensorSpec(shape=(batch_size, block_size), dtype=tf.int32),
    )
).prefetch(tf.data.AUTOTUNE)
```

The `output_signature` tells TensorFlow the shape and dtype of `x` and `y`. This matters because TensorFlow builds efficient computation graphs when it knows what kind of tensors will arrive.

`prefetch(tf.data.AUTOTUNE)` lets TensorFlow prepare future batches while the model trains on the current batch.

Metaphor: prefetching is a teaching assistant putting the next worksheet on each desk while the students are still finishing the current one.

## 4. Causal Self-Attention Layer

Causal self-attention lets each position ask, "Which previous characters should I pay attention to when predicting the next one?"

The class starts like this:

```python
class CausalSelfAttention(tf.keras.layers.Layer):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
```

`d_model` is the embedding width: the number of features used to represent each token position.

`n_heads` is the number of attention heads. Multiple heads let the model look for different kinds of relationships at the same time.

The assertion ensures the model dimension can be split evenly across heads. If `d_model = 64` and `n_heads = 4`, then:

```text
head_dim = 64 / 4 = 16
```

Metaphor: if the class has 64 pages of notes and 4 study groups, each group receives 16 pages. The split must be even.

### Q, K, and V projections

The layer creates two dense transformations.

```python
self.qkv = tf.keras.layers.Dense(3 * d_model)
self.proj = tf.keras.layers.Dense(d_model)
```

`self.qkv` creates three vectors for every token position:

- `q`: query, what this position is looking for.
- `k`: key, what this position offers as a label.
- `v`: value, the information this position contributes.

Metaphor: in a library, the query is the question you ask, the key is the catalog tag on each book, and the value is the book content you actually read.

`self.proj` mixes the attention output back into `d_model` features.

### Input shape

The `call` method receives `x`.

```python
def call(self, x):
    B = tf.shape(x)[0]
    T = tf.shape(x)[1]
    C = x.shape[-1]
```

The expected shape is:

```text
x: (B, T, C)
```

where:

- `B` is batch size.
- `T` is sequence length.
- `C` is channel width, normally equal to `d_model`.

For this script during training:

```text
B = 16
T = 32
C = 64
```

### Compute Q, K, V

The first dense layer produces all three tensors at once.

```python
qkv = self.qkv(x)
q, k, v = tf.split(qkv, 3, axis=-1)
```

Before the split:

```text
qkv: (B, T, 3 * d_model)
```

After the split:

```text
q: (B, T, d_model)
k: (B, T, d_model)
v: (B, T, d_model)
```

This is efficient because one matrix operation produces the query, key, and value representations.

### Split into heads

Each tensor is reshaped so attention can run separately in each head.

```python
q = tf.reshape(q, (B, T, self.n_heads, self.head_dim))
k = tf.reshape(k, (B, T, self.n_heads, self.head_dim))
v = tf.reshape(v, (B, T, self.n_heads, self.head_dim))
```

If `d_model = 64` and `n_heads = 4`, then:

```text
q: (B, T, 4, 16)
k: (B, T, 4, 16)
v: (B, T, 4, 16)
```

Then the dimensions are transposed:

```python
q = tf.transpose(q, [0, 2, 1, 3])
k = tf.transpose(k, [0, 2, 1, 3])
v = tf.transpose(v, [0, 2, 1, 3])
```

Now the shape is:

```text
(B, n_heads, T, head_dim)
```

This layout makes it easy to compute attention independently for each batch item and head.

### Attention scores

Attention scores compare queries to keys.

```python
att = tf.matmul(q, k, transpose_b=True) / tf.math.sqrt(tf.cast(self.head_dim, tf.float32))
```

The matrix multiplication compares every position with every other position.

Shape:

```text
q:   (B, n_heads, T, head_dim)
k^T: (B, n_heads, head_dim, T)
att: (B, n_heads, T, T)
```

For each row, `att[..., i, j]` asks:

```text
How much should position i attend to position j?
```

The division by `sqrt(head_dim)` keeps the dot products from becoming too large. Without this scaling, the softmax can become overly sharp early in training.

Metaphor: scaling is like lowering the volume before comparing many loud voices. It keeps one accidental shout from dominating the room.

### Causal mask

The causal mask prevents future information from leaking backward.

```python
mask = tf.linalg.band_part(tf.ones((T, T)), -1, 0)
```

This creates a lower-triangular matrix:

```text
1 0 0 0
1 1 0 0
1 1 1 0
1 1 1 1
```

A `1` means attention is allowed. A `0` means attention is blocked.

Position 0 can see only position 0. Position 1 can see positions 0 and 1. Position 2 can see positions 0, 1, and 2.

The mask is applied here:

```python
att = att * mask + (1.0 - mask) * (-1e10)
```

Blocked positions receive a very large negative number. After softmax, those positions become almost exactly zero probability.

Metaphor: the causal mask is an exam divider. A student may look at their own work and earlier notes, but not at future answer sheets.

### Softmax attention weights

The scores become probabilities.

```python
att = tf.nn.softmax(att, axis=-1)
```

After softmax, every row over the final dimension sums to approximately `1`. Each row is now a distribution over allowed previous positions.

Example for position 3:

```text
[0.10, 0.20, 0.60, 0.10, 0.00, 0.00, ...]
```

This means position 3 is mostly using information from position 2, while future positions remain blocked.

### Weighted sum of values

The attention weights choose a mixture of value vectors.

```python
out = tf.matmul(att, v)
```

Shape:

```text
att: (B, n_heads, T, T)
v:   (B, n_heads, T, head_dim)
out: (B, n_heads, T, head_dim)
```

The heads are then moved back and recombined:

```python
out = tf.transpose(out, [0, 2, 1, 3])
out = tf.reshape(out, (B, T, C))
```

The final projection returns the attention output:

```python
return self.proj(out)
```

Shape:

```text
(B, T, d_model)
```

The attention layer starts with one vector per token position and returns one improved vector per token position.

## 5. Transformer Block

A Transformer block improves token representations using two sublayers: attention and a feed-forward network.

```python
class Block(tf.keras.layers.Layer):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.att = CausalSelfAttention(d_model, n_heads)
        self.ff = tf.keras.Sequential([
            tf.keras.layers.Dense(4 * d_model, activation="relu"),
            tf.keras.layers.Dense(d_model)
        ])
        self.ln1 = tf.keras.layers.LayerNormalization()
        self.ln2 = tf.keras.layers.LayerNormalization()
```

The attention sublayer lets positions exchange information with previous positions.

The feed-forward sublayer processes each position independently after attention has mixed contextual information.

The feed-forward network expands the channel width to `4 * d_model`, applies ReLU, and compresses it back to `d_model`.

Metaphor: attention is the classroom discussion, where students listen to earlier remarks. The feed-forward network is private thinking time, where each student revises their own notes.

### Residual connections and layer normalization

The forward pass is:

```python
def call(self, x):
    x = x + self.att(self.ln1(x))
    x = x + self.ff(self.ln2(x))
    return x
```

This uses a pre-normalization Transformer style:

1. Normalize `x`.
2. Apply attention.
3. Add the result back to the original `x`.
4. Normalize again.
5. Apply the feed-forward network.
6. Add the result back again.

The additions are residual connections. They let the block modify the representation without forcing it to replace everything.

Metaphor: a residual connection is like editing in the margins instead of rewriting the whole essay. The original text remains available, and the new layer adds corrections.

Shape is preserved:

```text
input:  (B, T, d_model)
output: (B, T, d_model)
```

## 6. GPT Model

`TinyGPT` assembles the full character-level language model.

```python
class TinyGPT(tf.keras.Model):
    def __init__(self, vocab_size, d_model=64, n_heads=4, n_layers=2, block_size=32):
        super().__init__()
        self.block_size = block_size
```

Default hyperparameters:

```text
vocab_size = number of unique characters
d_model = 64
n_heads = 4
n_layers = 2
block_size = 32
```

This is small enough to train quickly, but large enough to show the architecture.

### Token embeddings

```python
self.tok_emb = tf.keras.layers.Embedding(vocab_size, d_model)
```

The token embedding maps each character id to a learned vector of length `64`.

If the input has shape:

```text
(B, T)
```

then token embeddings have shape:

```text
(B, T, d_model)
```

Metaphor: token embeddings are character costumes. The integer id is just a label; the embedding gives that character a learnable personality in vector space.

### Position embeddings

```python
self.pos_emb = tf.keras.layers.Embedding(block_size, d_model)
```

The Transformer needs position information because attention itself does not know whether a token came first, second, or tenth.

Position embeddings give each time step its own learned vector.

Metaphor: if token embeddings tell the model "what character is this?", position embeddings tell it "where is this character sitting in the row?"

### Transformer blocks and output head

```python
self.blocks = [Block(d_model, n_heads) for _ in range(n_layers)]
self.ln = tf.keras.layers.LayerNormalization()
self.head = tf.keras.layers.Dense(vocab_size)
```

`self.blocks` contains two Transformer blocks by default.

`self.ln` normalizes the final hidden states.

`self.head` maps each hidden vector to `vocab_size` output scores.

These output scores are called logits. A logit is not a probability. It is an unnormalized score that cross-entropy loss and softmax can consume.

Metaphor: logits are a scoreboard before converting scores into percentages.

### Forward pass

The model receives token ids:

```python
def call(self, x):
    B = tf.shape(x)[0]
    T = tf.shape(x)[1]
```

Shape:

```text
x: (B, T)
```

Token and position embeddings are created:

```python
tok = self.tok_emb(x)
pos = self.pos_emb(tf.range(T))
x = tok + pos
```

`tok` has shape:

```text
(B, T, d_model)
```

`pos` has shape:

```text
(T, d_model)
```

TensorFlow broadcasts `pos` across the batch dimension, so every example receives the same position information.

Then the hidden states pass through each Transformer block:

```python
for blk in self.blocks:
    x = blk(x)
```

Finally:

```python
x = self.ln(x)
return self.head(x)
```

The returned logits have shape:

```text
(B, T, vocab_size)
```

For every batch item and every time step, the model produces one score per possible next character.

## 7. Loss and Training

Training teaches the model to assign high scores to the actual next character.

```python
model = TinyGPT(vocab_size)
optimizer = tf.keras.optimizers.Adam(3e-4)
```

This creates the model and an Adam optimizer. Adam adjusts model weights using gradients from the loss.

The script then defines sparse categorical cross-entropy:

```python
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
```

This is the right loss because:

- The targets are integer token ids, not one-hot vectors.
- The model returns logits, not probabilities.

`from_logits=True` tells TensorFlow to apply the numerically stable version of softmax plus cross-entropy internally.

### Compile

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(3e-4),
    loss=loss_fn
)
```

This connects the model, optimizer, and loss into Keras's training loop.

Notice that the earlier `optimizer` variable is not reused. The script creates a new Adam optimizer inside `compile`. That is redundant but not harmful.

### Fit

```python
model.fit(
    dataset(),
    steps_per_epoch=2000,
    epochs=1
)
```

The dataset is infinite, so Keras needs `steps_per_epoch` to know when to stop. Here, one epoch means `2000` random batches.

Each training step does the following:

1. Get an input batch `x` and target batch `y`.
2. Run `x` through the model to get logits.
3. Compare logits against `y` with cross-entropy.
4. Compute gradients.
5. Update model weights with Adam.

Metaphor: the model writes an answer key for each worksheet, checks it against the real next characters, and adjusts its habits after every mistake.

Because the corpus is tiny, the model can memorize patterns quickly. That is useful for demonstration, but it is not evidence that the model has learned general English.

## 8. Generation

The original script labels this section as `8`. There is no separate code section `7`; the numbering simply skips from training to generation.

Generation uses the trained model autoregressively: predict one character, append it, then predict the next character from the updated text.

```python
def generate(model, start, max_new=200):
    idx = tf.convert_to_tensor([encode(start)], dtype=tf.int32)
```

`start` is the prompt. If `start = "hello"`, then `encode(start)` turns it into token ids.

The outer brackets create a batch dimension:

```text
idx: (1, prompt_length)
```

### One generation loop

The loop runs once per new character:

```python
for _ in range(max_new):
```

If `max_new = 200`, the function samples 200 additional characters.

The model only accepts up to `block_size` positions, so the context is cropped:

```python
idx_cond = idx[:, -block_size:]
```

This keeps the most recent 32 token ids.

Metaphor: the model has a short memory window. It can reread the last 32 characters, but not the whole scroll.

### Predict next-character logits

```python
logits = model.predict(idx_cond, verbose=0)
logits = logits[:, -1, :]
```

`model.predict(idx_cond)` returns logits for every position in the current context:

```text
(1, T, vocab_size)
```

Only the final position matters for the next generated character. That is why the script selects:

```text
logits[:, -1, :]
```

Now the shape is:

```text
(1, vocab_size)
```

This is the model's score for each possible next character after the full current prompt.

### Convert logits to probabilities

```python
probs = tf.nn.softmax(logits).numpy()
```

Softmax turns the logits into a probability distribution.

Example:

```python
chars = [' ', 'e', 'l', 'o']
probs = [0.10, 0.35, 0.40, 0.15]
```

This means the model currently believes `l` is the most likely next character, but it might still sample `e`, `o`, or a space.

### Sample one character

```python
next_id = np.random.choice(vocab_size, p=probs[0])
```

This samples one token id from the probability distribution.

Sampling is different from always taking the maximum probability. Sampling can produce variety. It can also produce strange text, especially when the model is tiny or poorly trained.

Metaphor: the model rolls a weighted die. The most likely character has the largest face, but lower-probability characters still have a chance.

### Append the sampled token

```python
next_id = tf.constant([[next_id]], dtype=tf.int32)
idx = tf.concat([idx, next_id], axis=1)
```

`next_id` is reshaped to `(1, 1)` so it can be concatenated to the current sequence.

After one loop:

```text
idx: (1, prompt_length + 1)
```

After 200 loops:

```text
idx: (1, prompt_length + 200)
```

Finally:

```python
return decode(idx.numpy()[0])
```

The generated token ids become a Python/NumPy array, the batch dimension is removed with `[0]`, and `decode` converts ids back into characters.

The script prints generated text:

```python
print(generate(model, "hello"))
```

## Walkthrough Example: One Training Window

Suppose the corpus starts:

```text
hello world
```

and `block_size = 5`.

One possible training example is:

```text
x text: hello
y text: ello_
```

The model sees:

```text
h e l l o
```

It is trained to predict:

```text
e l l o _
```

So the model receives several lessons at once:

| Position | Visible input because of causal mask | Target next character |
| -------- | ------------------------------------ | --------------------- |
| 0        | `h`                                  | `e`                   |
| 1        | `h e`                                | `l`                   |
| 2        | `h e l`                              | `l`                   |
| 3        | `h e l l`                            | `o`                   |
| 4        | `h e l l o`                          | space                 |

This table is the heart of causal language modeling. The model is never asked to predict a character using future characters.

## Walkthrough Example: One Generation Step

Assume the prompt is:

```text
hello
```

The function encodes it:

```text
[id_h, id_e, id_l, id_l, id_o]
```

The model produces logits for every prompt position, but generation keeps only the final row:

```text
scores for the character after "hello"
```

Softmax converts those scores into probabilities:

```text
space: 0.70
w:     0.20
t:     0.05
other: 0.05
```

If the sampled character is a space, the sequence becomes:

```text
hello_
```

Then the loop repeats. The model now predicts the character after `"hello "`.

## Important Tensor Shapes

These shapes are the skeleton of the program.

| Object                        | Shape                       | Meaning                     |
| ----------------------------- | --------------------------- | --------------------------- |
| `data`                        | `(num_characters,)`         | Full corpus as token ids    |
| `x`                           | `(batch_size, block_size)`  | Input token ids             |
| `y`                           | `(batch_size, block_size)`  | Next-character target ids   |
| `tok`                         | `(B, T, d_model)`           | Token embeddings            |
| `pos`                         | `(T, d_model)`              | Position embeddings         |
| `q`, `k`, `v` before heads    | `(B, T, d_model)`           | Query, key, value vectors   |
| `q`, `k`, `v` after transpose | `(B, n_heads, T, head_dim)` | Per-head representations    |
| `att`                         | `(B, n_heads, T, T)`        | Attention scores or weights |
| Transformer block output      | `(B, T, d_model)`           | Contextual token vectors    |
| model logits                  | `(B, T, vocab_size)`        | Next-character scores       |
| generation `idx`              | `(1, current_length)`       | Prompt plus sampled tokens  |

If one of these shapes is wrong, the model usually fails quickly. Shape discipline is the fastest way to debug Transformer code.

## Common Misunderstandings

### "The model predicts words."

This script predicts characters, not words. The token vocabulary contains individual characters such as `h`, `e`, space, and newline.

### "The target is the same as the input."

The target is shifted by one character. If the input is `hello`, the target is `ello `. The task is next-character prediction.

### "The model can look at the whole sequence."

The causal mask prevents each position from seeing future positions. This is essential. Without the mask, the model could cheat during training by reading the answer.

### "Softmax should be applied before the loss."

The model returns logits. The loss uses `from_logits=True`, so TensorFlow applies the stable softmax-cross-entropy calculation internally.

### "Generated text proves the model understands language."

Generated text from this script proves only that the training and sampling loop runs. The corpus is far too small for general language understanding.

### "More training always makes it better."

On this tiny corpus, more training mostly improves memorization. It may make the model echo the training text more strongly, not generalize better.

## What Students Should Take Away

This script is small, but it contains the core causal language-model pipeline.

The essential mechanism is:

```text
text -> token ids -> shifted batches -> causal Transformer -> logits -> cross-entropy -> sampled next tokens
```

If you understand why `x` and `y` are shifted, why the mask is lower triangular, why logits have shape `(B, T, vocab_size)`, and why generation appends one sampled token at a time, then you understand the working skeleton of a GPT-style model.
