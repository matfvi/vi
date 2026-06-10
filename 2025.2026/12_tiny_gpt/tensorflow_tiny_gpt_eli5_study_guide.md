# TensorFlow Tiny GPT ELI5 Study Guide

This is a companion guide for `tensorflow_tiny_gpt_explained.md`.
It follows the same sections, but explains the ideas in simpler language,
with key concepts, important keywords, and metaphors.

The whole script is about one task:

> Given the characters already seen, guess the next character.

The model is tiny, character-level, and trained on a very small text. It is
useful because it shows the same basic pipeline used by larger GPT-style
language models.

## The Big Picture

**ELI5 explanation:** The program teaches a small neural network to continue
text. First it turns characters into numbers. Then it cuts the text into short
practice examples. Then it trains a Transformer to guess the next character in
each example. Finally, it generates new text by guessing one character at a
time.

**Key concept:** A GPT-style model is a next-token predictor. In this script,
the tokens are characters.

**Important keywords:**

- `character-level`: the model works with individual characters, not words.
- `token id`: a number that stands for one character.
- `shifted text window`: an input sequence paired with the same sequence moved
  one character forward.
- `causal`: the model is not allowed to look at future characters.
- `autoregressive`: the model generates by feeding its own output back into
  itself.
- `decoder-only`: the Transformer uses the GPT-style architecture that predicts
  from previous tokens.

**Metaphor:** The model is a student with a tiny book. The teacher covers the
next letter and asks, "What comes next?" The student practices this again and
again.

**Common pitfall:** The model is not learning all of English. It is learning
patterns from only the tiny text it was given.

## 1. Imports

**ELI5 explanation:** The script brings in two toolboxes. NumPy helps prepare
the data. TensorFlow builds and trains the neural network.

**Key concept:** Imports give the script access to external libraries.

**Important keywords:**

- `import`: load a library so the script can use it.
- `tensorflow as tf`: TensorFlow is used for layers, tensors, training, loss,
  and optimization.
- `numpy as np`: NumPy is used for arrays, random indexes, stacking examples,
  and simple preprocessing.

**Metaphor:** NumPy is the desk where you cut paper worksheets. TensorFlow is
the classroom where the model practices on those worksheets.

**Common pitfall:** NumPy arrays and TensorFlow tensors are similar, but they
are not the same object type. NumPy is mostly used before training, while
TensorFlow is used inside the model and training loop.

## 2. Tiny Corpus

**ELI5 explanation:** The corpus is the only text the model studies. If a
pattern does not appear in this text, the model has no outside knowledge of it.

**Key concept:** Training data defines what the model can learn.

**Important keywords:**

- `corpus`: the full text used for training.
- `text`: the string that contains the tiny dataset.
- `triple quotes`: Python syntax for a multi-line string.
- `newline character`: the hidden line-break character included in the string.

**Metaphor:** The corpus is the model's whole textbook. If the textbook is
short, the model's knowledge is short too.

**Common pitfall:** Newline characters count as real characters. They are part
of the vocabulary and can be predicted during generation.

### Vocabulary

**ELI5 explanation:** The vocabulary is the list of different characters that
appear in the text. The model can only read and write characters from this
list.

**Key concept:** The vocabulary defines the model's alphabet.

**Important keywords:**

- `set(text)`: removes duplicate characters.
- `sorted(...)`: puts characters in a stable order.
- `chars`: the sorted list of unique characters.
- `vocab_size`: the number of unique characters.

**Metaphor:** The vocabulary is a tray of letter tiles. If a tile is not in the
tray, the model cannot place it on the board.

**Common pitfall:** `vocab_size` is not the number of characters in the full
text. It is the number of different character types.

### Character-to-id and id-to-character maps

**ELI5 explanation:** Neural networks work with numbers, so the script needs a
dictionary that turns each character into a number. It also needs the reverse
dictionary so generated numbers can become text again.

**Key concept:** Tokenization creates a two-way bridge between text and
numbers.

**Important keywords:**

- `stoi`: "string to integer"; maps each character to its token id.
- `itos`: "integer to string"; maps each token id back to a character.
- `enumerate(chars)`: gives each character an index.
- `dictionary`: a lookup table from keys to values.

**Metaphor:** `stoi` is a coat-check desk that gives each character a numbered
ticket. `itos` uses the ticket to return the original character.

**Common pitfall:** The ids are arbitrary labels. Token id `0` is not
"smaller" or "less important" than token id `5`.

### Encoding and decoding

**ELI5 explanation:** Encoding turns text into token ids. Decoding turns token
ids back into text.

**Key concept:** The model trains on encoded data, not raw strings.

**Important keywords:**

- `encode(s)`: converts a string into a NumPy array of integer ids.
- `decode(l)`: converts a list or array of ids back into a string.
- `dtype=np.int32`: stores ids as 32-bit integers.
- `data`: the full corpus after encoding.

**Metaphor:** Encoding is translating a sentence into secret numbers. Decoding
is using the codebook to turn the secret numbers back into letters.

**Common pitfall:** `encode` can only handle characters already in `stoi`. A
new unknown character would not have an id.

## 3. Batch Generator

**ELI5 explanation:** The batch generator makes practice problems. Each problem
is a short slice of text. The model sees the slice and tries to predict the
next character at every position.

**Key concept:** Training uses many small windows from the corpus instead of
feeding the whole text as one example.

**Important keywords:**

- `block_size`: how many characters are in one training window.
- `batch_size`: how many windows are trained together.
- `batch`: a group of examples processed in one training step.
- `shape`: the size of each tensor dimension.

**Metaphor:** The corpus is a long strip of paper. The batch generator cuts out
many short strips and hands them to the model as worksheets.

**Common pitfall:** `block_size` is context length, not vocabulary size.

### Random window starts

**ELI5 explanation:** The script chooses random places in the encoded text.
Each chosen place becomes the start of one training example.

**Key concept:** Random sampling gives the model many different local contexts.

**Important keywords:**

- `np.random.randint(...)`: chooses random integer start positions.
- `ix`: the array of random start indexes.
- `len(data) - block_size - 1`: leaves enough room for the input window and
  the shifted target window.
- `size=batch_size`: creates one start index per example in the batch.

**Metaphor:** Imagine closing your eyes and pointing to random places on a long
sentence, then copying the next 32 characters from each place.

**Common pitfall:** The high endpoint of `np.random.randint` is excluded. The
source notes that this leaves the final possible window unused, which is
harmless for this teaching script.

### Inputs and targets

**ELI5 explanation:** `x` is what the model reads. `y` is the answer key: the
next character after each position in `x`.

**Key concept:** The target is the input shifted one step into the future.

**Important keywords:**

- `x`: input token ids.
- `y`: target token ids.
- `np.stack(...)`: combines many windows into one batch array.
- `data[i:i+block_size]`: the input slice.
- `data[i+1:i+block_size+1]`: the next-character target slice.

**Metaphor:** `x` is a row of covered flashcards the model can see. `y` is the
teacher's answer sheet showing the next card after each visible card.

**Common pitfall:** `x` and `y` look almost the same, but they are not the same.
`y` is moved one character forward.

### TensorFlow dataset

**ELI5 explanation:** TensorFlow needs a steady stream of batches. The dataset
function wraps the Python batch generator so Keras can ask for new batches
during training.

**Key concept:** `tf.data.Dataset` turns batch creation into an input pipeline.

**Important keywords:**

- `gen()`: an infinite Python generator that yields `(x, y)` forever.
- `yield`: gives one batch to TensorFlow, then continues later.
- `tf.data.Dataset.from_generator`: builds a TensorFlow dataset from `gen`.
- `output_signature`: tells TensorFlow the shape and dtype of each batch.
- `tf.TensorSpec`: describes one tensor expected from the generator.
- `prefetch(tf.data.AUTOTUNE)`: prepares future batches while training uses the
  current one.

**Metaphor:** The dataset is a conveyor belt. The model takes one worksheet
from the belt while TensorFlow prepares the next worksheet behind the scenes.

**Common pitfall:** Because `gen()` is infinite, training must specify
`steps_per_epoch`. Otherwise Keras would not know when an epoch ends.

## 4. Causal Self-Attention Layer

**ELI5 explanation:** Self-attention lets each position decide which earlier
positions are useful. Causal self-attention adds one rule: a position cannot
look ahead at future positions.

**Key concept:** Attention mixes information across time while the causal mask
prevents cheating.

**Important keywords:**

- `CausalSelfAttention`: custom TensorFlow layer for masked self-attention.
- `d_model`: width of each token representation.
- `n_heads`: number of separate attention heads.
- `head_dim`: number of features per head.
- `assert d_model % n_heads == 0`: checks that `d_model` splits evenly across
  heads.

**Metaphor:** Each character is a student writing an answer. The student may
listen to students who spoke earlier, but not to students who will speak later.

**Common pitfall:** Attention does not automatically know time order. The
causal mask enforces the direction of information.

### Q, K, and V projections

**ELI5 explanation:** Each token position creates three versions of itself:
what it is looking for, what label it offers, and what information it can give.

**Key concept:** Query-key matching decides attention weights; values carry the
information that gets mixed.

**Important keywords:**

- `q`: query; what this position is searching for.
- `k`: key; what each position advertises about itself.
- `v`: value; the information each position contributes.
- `Dense(3 * d_model)`: creates Q, K, and V together.
- `Dense(d_model)`: projects the attention result back to the model width.

**Metaphor:** In a library, the query is your question, the key is each book's
catalog label, and the value is the page content you actually read.

**Common pitfall:** Keys and values are different. Keys help choose where to
look; values are what gets copied and mixed after choosing.

### Input shape

**ELI5 explanation:** The attention layer receives a 3D tensor. The dimensions
mean: which example, which time position, and which feature.

**Key concept:** Attention expects hidden vectors, not raw token ids.

**Important keywords:**

- `B`: batch size.
- `T`: sequence length.
- `C`: channel width, usually `d_model`.
- `(B, T, C)`: the shape of the input to the attention layer.
- `tf.shape(x)`: reads dynamic tensor dimensions.
- `x.shape[-1]`: reads the static final dimension when available.

**Metaphor:** Think of a spreadsheet stack. `B` chooses the worksheet, `T`
chooses the row in that worksheet, and `C` chooses the columns of features.

**Common pitfall:** Raw input batches have shape `(B, T)`. After embeddings,
they become `(B, T, d_model)`.

### Compute Q, K, V

**ELI5 explanation:** The layer runs one dense transformation and then cuts the
result into three equal parts: Q, K, and V.

**Key concept:** One combined projection is an efficient way to compute all
three attention tensors.

**Important keywords:**

- `qkv = self.qkv(x)`: computes the combined tensor.
- `tf.split(qkv, 3, axis=-1)`: splits the last dimension into three parts.
- `(B, T, 3 * d_model)`: shape before splitting.
- `(B, T, d_model)`: shape of each of `q`, `k`, and `v` after splitting.

**Metaphor:** One machine prints three connected tickets, then the script cuts
them apart into query, key, and value tickets.

**Common pitfall:** Q, K, and V start from the same input `x`, but the dense
layer learns different weights for each part.

### Split into heads

**ELI5 explanation:** The script divides each token vector into several smaller
parts called heads. Each head can learn a different kind of relationship.

**Key concept:** Multi-head attention runs several attention calculations in
parallel.

**Important keywords:**

- `tf.reshape`: changes the tensor view into `(B, T, n_heads, head_dim)`.
- `tf.transpose`: reorders dimensions into `(B, n_heads, T, head_dim)`.
- `n_heads`: number of attention groups.
- `head_dim`: feature width for each head.

**Metaphor:** Instead of one big study group, the class splits into smaller
groups. One group may track spaces, another may track repeated letters, and
another may track line breaks.

**Common pitfall:** Reshape does not create new meaning by itself. The learned
dense weights make the per-head features useful.

### Attention scores

**ELI5 explanation:** Each query is compared with each key. The result is a
score saying how much one position should care about another position.

**Key concept:** Dot products measure query-key compatibility.

**Important keywords:**

- `tf.matmul(q, k, transpose_b=True)`: compares every query with every key.
- `att`: attention scores before softmax.
- `(B, n_heads, T, T)`: one score for every pair of positions.
- `sqrt(head_dim)`: scaling factor that keeps scores controlled.

**Metaphor:** Every student asks, "Whose notes match what I need?" The score is
how useful each other student's notes seem.

**Common pitfall:** These scores are not probabilities yet. They become
probabilities only after softmax.

### Causal mask

**ELI5 explanation:** The mask blocks attention to future positions. It lets a
token use itself and earlier tokens only.

**Key concept:** The lower-triangular mask preserves next-token prediction.

**Important keywords:**

- `tf.linalg.band_part`: creates the lower-triangular mask.
- `mask`: a matrix of allowed and blocked positions.
- `1`: attention allowed.
- `0`: attention blocked.
- `-1e10`: a very negative score that softmax turns into near-zero
  probability.

**Metaphor:** The mask is a privacy screen during a test. You may read your own
answer and earlier notes, but future answer sheets are covered.

**Common pitfall:** Without the mask, training would be too easy because the
model could look directly at future characters.

### Softmax attention weights

**ELI5 explanation:** Softmax turns attention scores into percentages. For each
position, the allowed attention weights add up to about 1.

**Key concept:** Softmax converts raw scores into a distribution over previous
positions.

**Important keywords:**

- `tf.nn.softmax(att, axis=-1)`: normalizes scores across the final dimension.
- `axis=-1`: apply softmax across the keys each query can attend to.
- `attention weights`: probabilities that say how much to use each value.
- `distribution`: a list of nonnegative weights that sum to 1.

**Metaphor:** The model has one dollar of attention to spend. Softmax decides
how many cents go to each previous position.

**Common pitfall:** Softmax is applied inside attention here, but the model's
final output head still returns logits for the loss.

### Weighted sum of values

**ELI5 explanation:** The attention weights are used to mix the value vectors.
High-weight positions contribute more. Low-weight positions contribute less.

**Key concept:** Attention output is a weighted blend of value information.

**Important keywords:**

- `tf.matmul(att, v)`: combines attention weights with values.
- `out`: the mixed value vectors.
- `tf.transpose(out, [0, 2, 1, 3])`: moves heads back after sequence positions.
- `tf.reshape(out, (B, T, C))`: recombines all heads into one vector per
  position.
- `self.proj(out)`: mixes the recombined result back into `d_model` features.

**Metaphor:** Each student copies a little from several earlier notebooks,
using more from the notebooks that seemed most relevant.

**Common pitfall:** The attention layer returns the same outer shape it
received: `(B, T, d_model)`.

## 5. Transformer Block

**ELI5 explanation:** A Transformer block has two jobs. Attention lets each
position gather context from earlier positions. The feed-forward network lets
each position process its own updated information.

**Key concept:** A block improves token representations while keeping the same
shape.

**Important keywords:**

- `Block`: one Transformer block.
- `self.att`: the causal self-attention sublayer.
- `self.ff`: the feed-forward sublayer.
- `Dense(4 * d_model, activation="relu")`: expands features and applies a
  nonlinear function.
- `Dense(d_model)`: compresses features back to the model width.
- `LayerNormalization`: normalizes feature values for stable training.

**Metaphor:** Attention is group discussion. The feed-forward network is quiet
thinking time after the discussion.

**Common pitfall:** The feed-forward layer works separately at each position.
Position-to-position mixing happens in attention.

### Residual connections and layer normalization

**ELI5 explanation:** The block does not throw away the old representation. It
adds the attention result to it, then adds the feed-forward result too.

**Key concept:** Residual connections let each layer make changes without
erasing the original signal.

**Important keywords:**

- `x + ...`: residual addition.
- `self.ln1(x)`: first layer normalization before attention.
- `self.ln2(x)`: second layer normalization before feed-forward.
- `pre-normalization`: normalize before each sublayer.
- `(B, T, d_model)`: the shape before and after the block.

**Metaphor:** A residual connection is editing in the margins. The original
essay is still there, and the new notes are added beside it.

**Common pitfall:** Residual connections require matching shapes. That is why
attention and feed-forward both return `d_model` width.

## 6. GPT Model

**ELI5 explanation:** `TinyGPT` puts the full model together. It starts with
token ids, turns them into vectors, adds position information, passes them
through Transformer blocks, and returns scores for the next character.

**Key concept:** The model maps `(B, T)` token ids to `(B, T, vocab_size)`
logits.

**Important keywords:**

- `TinyGPT`: the full Keras model.
- `vocab_size`: number of possible output characters.
- `d_model=64`: hidden vector width.
- `n_heads=4`: number of attention heads.
- `n_layers=2`: number of Transformer blocks.
- `block_size=32`: maximum context length.

**Metaphor:** The GPT model is an assembly line: ids enter, embeddings dress
them up, blocks refine them, and the head produces next-character scores.

**Common pitfall:** `block_size` limits how much recent context generation can
use.

### Token embeddings

**ELI5 explanation:** Token embeddings turn each character id into a learned
vector. The id is just a label; the embedding is the useful representation.

**Key concept:** Embeddings let the model learn features for each character.

**Important keywords:**

- `Embedding(vocab_size, d_model)`: lookup table from token id to vector.
- `tok_emb`: token embedding layer.
- `(B, T)`: input ids shape.
- `(B, T, d_model)`: token embedding output shape.

**Metaphor:** A token id is a locker number. The embedding is what is inside
the locker.

**Common pitfall:** Embeddings are learned during training. They are not
hand-written character meanings.

### Position embeddings

**ELI5 explanation:** Attention sees a bag of vectors unless the model is told
where each token sits. Position embeddings add information about first,
second, third, and later positions.

**Key concept:** The model needs position information to understand order.

**Important keywords:**

- `pos_emb`: position embedding layer.
- `Embedding(block_size, d_model)`: lookup table from position index to vector.
- `tf.range(T)`: creates position indexes from `0` to `T - 1`.
- `tok + pos`: combines character identity with position.
- `broadcasting`: TensorFlow automatically shares `pos` across the batch.

**Metaphor:** Token embeddings say what letter is sitting there. Position
embeddings say which chair the letter is sitting in.

**Common pitfall:** Position embeddings are limited by `block_size`. The model
does not have learned positions beyond that size.

### Transformer blocks and output head

**ELI5 explanation:** The model runs the embeddings through several Transformer
blocks, normalizes the result, and then uses a final dense layer to score every
possible next character.

**Key concept:** The output head converts hidden vectors into vocabulary-sized
logits.

**Important keywords:**

- `self.blocks`: list of Transformer blocks.
- `self.ln`: final layer normalization.
- `self.head`: final dense layer.
- `logits`: raw, unnormalized scores.
- `vocab_size`: number of scores produced at each position.

**Metaphor:** The Transformer blocks are editors improving a draft. The output
head is the judge that scores every possible next character.

**Common pitfall:** Logits are not probabilities. They can be negative, large,
or small. Softmax or cross-entropy interprets them later.

### Forward pass

**ELI5 explanation:** The forward pass is what happens when data moves through
the model. Token ids become embeddings, positions are added, blocks process the
vectors, and the head returns logits.

**Key concept:** Every time step gets its own next-character score list.

**Important keywords:**

- `call(self, x)`: defines the model's forward pass.
- `B`: number of examples in the batch.
- `T`: number of token positions in each example.
- `tok`: token embeddings.
- `pos`: position embeddings.
- `for blk in self.blocks`: run each Transformer block in order.
- `(B, T, vocab_size)`: final logits shape.

**Metaphor:** The forward pass is a factory belt. Each station changes the
representation a little, then passes it to the next station.

**Common pitfall:** The model returns logits for every position, even though
generation usually uses only the final position.

## 7. Loss and Training

**ELI5 explanation:** Training compares the model's guesses with the real next
characters. If the guesses are wrong, the optimizer nudges the model weights so
future guesses improve.

**Key concept:** Cross-entropy trains the model to give high logits to the true
next character.

**Important keywords:**

- `model = TinyGPT(vocab_size)`: creates the model.
- `Adam`: optimizer that updates model weights.
- `3e-4`: learning rate.
- `SparseCategoricalCrossentropy`: loss for integer class labels.
- `from_logits=True`: tells the loss that the model outputs raw logits.
- `gradient`: information about how to change weights to reduce loss.

**Metaphor:** The model takes a quiz, checks the answer key, and adjusts its
study habits after every mistake.

**Common pitfall:** The small corpus makes memorization easy. Lower loss does
not mean the model understands general language.

### Compile

**ELI5 explanation:** `compile` connects the model, optimizer, and loss so
Keras knows how to train.

**Key concept:** Keras needs a training recipe before `fit` can run.

**Important keywords:**

- `model.compile(...)`: configures the training loop.
- `optimizer`: decides how weights are updated.
- `loss`: measures how wrong the model is.
- `from_logits=True`: avoids manually applying softmax before the loss.

**Metaphor:** `compile` is filling out the training form: who is the student,
who grades the quiz, and how corrections are made.

**Common pitfall:** The script creates an `optimizer` variable and then creates
a new Adam optimizer inside `compile`. That is redundant but harmless.

### Fit

**ELI5 explanation:** `fit` runs the actual training loop. For each step, it
gets a batch, predicts logits, computes loss, calculates gradients, and updates
weights.

**Key concept:** `steps_per_epoch` controls how many batches are used because
the dataset is infinite.

**Important keywords:**

- `model.fit(...)`: starts Keras training.
- `dataset()`: supplies batches forever.
- `steps_per_epoch=2000`: stops the epoch after 2000 batches.
- `epochs=1`: run one epoch.
- `batch`: one group of training windows.
- `weights`: learned numbers inside the model.

**Metaphor:** `fit` is 2000 rounds of practice worksheets. After each round,
the student sees what was wrong and adjusts.

**Common pitfall:** One epoch here does not mean one pass over the corpus. The
dataset samples random batches forever, so one epoch means the chosen number of
steps.

## 8. Generation

**ELI5 explanation:** Generation starts with a prompt. The model predicts the
next character, samples one, appends it, and repeats.

**Key concept:** Autoregressive generation turns a next-character predictor
into a text generator.

**Important keywords:**

- `generate(model, start, max_new=200)`: function that creates new text.
- `start`: prompt text.
- `max_new`: number of new characters to sample.
- `idx`: token ids for the prompt plus generated characters.
- `tf.convert_to_tensor`: converts encoded ids into a TensorFlow tensor.

**Metaphor:** The model writes one letter, reads the updated sentence, writes
one more letter, and keeps going.

**Common pitfall:** Every new character depends on previous sampled characters.
One strange sample can affect later samples.

### One generation loop

**ELI5 explanation:** The loop runs once for every new character. Before each
prediction, it crops the context to the most recent `block_size` tokens.

**Key concept:** The model has a fixed-size context window.

**Important keywords:**

- `for _ in range(max_new)`: repeat once per generated character.
- `idx[:, -block_size:]`: keep only the most recent context tokens.
- `idx_cond`: cropped context passed to the model.
- `context window`: the text the model can currently use.

**Metaphor:** The model has a small desk. It can keep the last 32 character
cards on the desk, but older cards fall off the back.

**Common pitfall:** The returned generated text can be longer than
`block_size`, but each prediction only sees the most recent `block_size`
tokens.

### Predict next-character logits

**ELI5 explanation:** The model produces scores for every position in the
current context, but generation only needs the scores after the final position.

**Key concept:** The last row of logits answers, "What comes after the full
current prompt?"

**Important keywords:**

- `model.predict(idx_cond, verbose=0)`: runs the model without training.
- `logits`: raw next-character scores.
- `logits[:, -1, :]`: select the final time step.
- `(1, T, vocab_size)`: full prediction shape.
- `(1, vocab_size)`: final-position logits shape.

**Metaphor:** The model writes a score sheet after every character, but we only
read the score sheet at the end of the current sentence.

**Common pitfall:** Using all positions for generation would be wrong. The next
new character should come from the final context position.

### Convert logits to probabilities

**ELI5 explanation:** Softmax turns raw scores into probabilities so the script
can sample a character.

**Key concept:** Generation needs a probability distribution over the
vocabulary.

**Important keywords:**

- `tf.nn.softmax(logits)`: converts logits to probabilities.
- `.numpy()`: converts the TensorFlow tensor to a NumPy array.
- `probs`: probability for each possible next character.
- `vocab_size`: length of the probability list.

**Metaphor:** Logits are judge scores. Softmax turns the scores into a pie
chart.

**Common pitfall:** The most likely character may not always be chosen, because
the script samples from the distribution.

### Sample one character

**ELI5 explanation:** The script randomly chooses one character id, but the
random choice is weighted by the model's probabilities.

**Key concept:** Sampling creates variety.

**Important keywords:**

- `np.random.choice(vocab_size, p=probs[0])`: choose one token id according to
  probabilities.
- `next_id`: sampled next token id.
- `p=probs[0]`: probability weights for the random choice.
- `argmax`: the alternative strategy of always taking the highest probability,
  which this script does not use.

**Metaphor:** The model rolls a weighted die. Common characters have bigger
faces on the die, but smaller faces can still land.

**Common pitfall:** Sampling can produce strange text, especially with a tiny
model and tiny training corpus.

### Append the sampled token

**ELI5 explanation:** The sampled id is reshaped so it can be attached to the
current sequence. Then the loop continues with the longer sequence.

**Key concept:** Generated tokens become future context.

**Important keywords:**

- `tf.constant([[next_id]], dtype=tf.int32)`: creates a `(1, 1)` tensor for the
  sampled token.
- `tf.concat([idx, next_id], axis=1)`: appends the token along the time axis.
- `axis=1`: the sequence-length dimension.
- `decode(idx.numpy()[0])`: converts the final ids back to text.

**Metaphor:** Each sampled character is added to the end of the paper strip.
The model reads the longer strip before choosing the next character.

**Common pitfall:** The batch dimension stays even for one prompt. That is why
the generated ids have shape `(1, current_length)`.

## Walkthrough Example: One Training Window

**ELI5 explanation:** A training window teaches several next-character lessons
at once. If `x` is `hello`, then `y` is `ello `.

**Key concept:** At each position, the visible prefix predicts the next
character.

**Important keywords:**

- `x text`: the visible input sequence.
- `y text`: the shifted next-character answers.
- `position`: one place in the sequence.
- `visible input`: what the causal mask allows the model to use.
- `target next character`: the correct answer for that position.

**Metaphor:** The teacher shows more and more of a word: `h`, then `he`, then
`hel`, and asks the student to guess the next character each time.

**Common pitfall:** The model is not asked to reconstruct the same text. It is
asked to predict the next character after each prefix.

## Walkthrough Example: One Generation Step

**ELI5 explanation:** If the prompt is `hello`, the model scores possible next
characters after `hello`. Softmax turns scores into probabilities. Sampling
chooses one character, such as a space. The prompt then becomes `hello `, and
the loop repeats.

**Key concept:** Generation uses only the final-position prediction from the
current context.

**Important keywords:**

- `prompt`: starting text given to the model.
- `final row`: logits for the next character after the whole prompt.
- `probabilities`: softmax-normalized scores.
- `sampled character`: the token chosen from the probabilities.
- `updated sequence`: prompt plus the sampled character.

**Metaphor:** It is like autocomplete pressing one key at a time. After each
key, the suggestion list changes.

**Common pitfall:** Generation is sequential. The model does not generate all
200 characters in one independent step.

## Important Tensor Shapes

**ELI5 explanation:** Shapes tell you how data is arranged. If the shape is
wrong, the model usually fails quickly.

**Key concept:** Transformer code is easier to debug when every tensor shape is
known.

**Important keywords:**

- `data`: `(num_characters,)`; the whole corpus as ids.
- `x`: `(batch_size, block_size)`; input token ids.
- `y`: `(batch_size, block_size)`; next-character target ids.
- `tok`: `(B, T, d_model)`; token embeddings.
- `pos`: `(T, d_model)`; position embeddings.
- `q`, `k`, `v` before heads: `(B, T, d_model)`.
- `q`, `k`, `v` after transpose: `(B, n_heads, T, head_dim)`.
- `att`: `(B, n_heads, T, T)`; attention scores or weights.
- `logits`: `(B, T, vocab_size)`; next-character scores.
- `idx`: `(1, current_length)`; prompt plus generated tokens.

**Metaphor:** Shapes are the labels on storage boxes. If you put a wide object
into a narrow box, the program complains.

**Common pitfall:** `T` can be smaller than `block_size` during generation if
the prompt is short. It is the current sequence length passed to the model.

## Common Misunderstandings

This section corrects the mistakes students most often make when reading this
script.

### "The model predicts words."

**ELI5 explanation:** It predicts characters. A space is a character. A newline
is a character. The word `hello` is five separate predictions.

**Key concept:** Token choice defines the prediction unit.

**Important keywords:** `character-level`, `token`, `vocabulary`, `id`.

**Metaphor:** The model builds text from letter tiles, not word blocks.

### "The target is the same as the input."

**ELI5 explanation:** The target is almost the same as the input, but shifted
one character ahead.

**Key concept:** Shifted targets create the next-character task.

**Important keywords:** `x`, `y`, `shift`, `next character`, `target`.

**Metaphor:** `x` is today's calendar, and `y` is tomorrow's calendar moved one
slot forward.

### "The model can look at the whole sequence."

**ELI5 explanation:** A position can only look at itself and earlier positions.
The causal mask blocks future positions.

**Key concept:** Future information would let the model cheat during training.

**Important keywords:** `causal mask`, `lower triangular`, `future`, `leak`.

**Metaphor:** The answer key is folded so the student cannot see answers that
come later.

### "Softmax should be applied before the loss."

**ELI5 explanation:** The model gives logits to the loss. Because
`from_logits=True`, TensorFlow handles the stable softmax-cross-entropy
calculation internally.

**Key concept:** Do not softmax twice.

**Important keywords:** `logits`, `softmax`, `cross-entropy`,
`from_logits=True`.

**Metaphor:** Give the raw exam scores to the grading calculator. The
calculator knows how to convert them.

### "Generated text proves the model understands language."

**ELI5 explanation:** Generated text only proves the model learned enough local
patterns to produce characters. This tiny script does not prove understanding.

**Key concept:** Text-like output is not the same as language understanding.

**Important keywords:** `generation`, `sampling`, `training corpus`,
`memorization`.

**Metaphor:** A student can mimic a short poem after reading it many times
without understanding poetry.

### "More training always makes it better."

**ELI5 explanation:** On a tiny corpus, more training mostly makes the model
memorize the training text more strongly.

**Key concept:** More optimization can improve training loss without improving
generalization.

**Important keywords:** `overfitting`, `memorization`, `generalization`,
`tiny corpus`.

**Metaphor:** Reading one flashcard 10,000 times makes you good at that
flashcard, not at the whole subject.

## What Students Should Take Away

**ELI5 explanation:** The script is small, but it shows the full loop: text
becomes ids, ids become training windows, a causal Transformer predicts next
characters, loss updates the model, and generation samples one new character at
a time.

**Key concept:** GPT-style modeling is next-token prediction with a causal
context.

**Important keywords:**

- `text -> token ids`: convert language data into numbers.
- `shifted batches`: create input and target examples.
- `causal Transformer`: process previous context without future leakage.
- `logits`: next-character scores.
- `cross-entropy`: training signal.
- `sampled next tokens`: generation output.

**Metaphor:** The whole program is an autocomplete school. The model studies a
tiny book, practices guessing the next letter, gets graded, and then writes by
choosing one letter at a time.

**Final checkpoint:** If you can explain why `x` and `y` are shifted, why the
mask is lower triangular, why logits have shape `(B, T, vocab_size)`, and why
generation appends one sampled token at a time, you understand the working
skeleton of this tiny GPT.

## Quick Keyword Glossary

Use this as a compact review list.

| Keyword | ELI5 meaning |
| --- | --- |
| `token` | One piece of text the model handles. Here, one character. |
| `token id` | A number that represents one token. |
| `vocab_size` | Number of different tokens the model can output. |
| `stoi` | Lookup from character to integer id. |
| `itos` | Lookup from integer id to character. |
| `encode` | Turn text into ids. |
| `decode` | Turn ids back into text. |
| `block_size` | Maximum number of recent characters used as context. |
| `batch_size` | Number of training windows processed together. |
| `B` | Batch size dimension. |
| `T` | Time or sequence-length dimension. |
| `C` | Channel or feature-width dimension. |
| `d_model` | Width of the model's hidden vectors. |
| `n_heads` | Number of attention heads. |
| `head_dim` | Width of each attention head. |
| `Q` / `query` | What a position is looking for. |
| `K` / `key` | What a position advertises for matching. |
| `V` / `value` | Information a position contributes. |
| `attention score` | Raw query-key match score. |
| `causal mask` | Rule that blocks future positions. |
| `softmax` | Converts scores into probabilities. |
| `embedding` | Learned vector for a token or position. |
| `residual connection` | Adds a layer's result back to its input. |
| `LayerNormalization` | Stabilizes feature values inside the model. |
| `logit` | Raw output score before probability conversion. |
| `cross-entropy` | Loss that rewards high score on the correct class. |
| `from_logits=True` | Tells TensorFlow the loss receives raw logits. |
| `Adam` | Optimizer that updates model weights. |
| `autoregressive` | Generates by feeding previous outputs back in. |
| `generation` | Sampling new tokens from the trained model. |
