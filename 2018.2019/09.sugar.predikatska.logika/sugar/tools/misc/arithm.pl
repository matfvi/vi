#!/usr/bin/perl
##
## Converts Cryptarithmetic Puzzle into Sugar CSP
##
## This program is a part of Sugar (a SAT-based Constraint Solver)
## software package.
##     http://bach.istc.kobe-u.ac.jp/sugar/
## (C) Naoyuki Tamura
##
use Getopt::Std;
use strict;
$| = 1;

use vars qw($opt_h);

&getopts("h");

if ($opt_h) {
    print "Example: $0 SEND MORE MONEY >file.csp\n";
    exit(1);
}

my @words = @ARGV;

print "; Crypt arithmetic puzzle ", join(" ", @words), "\n";
&write_csp();
print "; END\n";
exit 0;

sub write_csp {
    my $base = 10;
    my %chars = ();
    foreach my $word (@words) {
	my @w = split(//, $word);
	foreach my $c (@w) {
	    if ($c !~ /^[a-zA-Z]$/) {
		die "non-alphabet character";
	    }
	    $chars{$c} = 1;
	}
	$word = \@w;
    }
    foreach my $word (@words) {
	$chars{$word->[0]} = -1;
    }
    my @chars = sort keys %chars;
    if (scalar(@chars) > $base) {
	die "too many characters";
    }
    foreach my $c (@chars) {
	my $min = $chars{$c} > 0 ? 0 : 1;
	my $max = $base - 1;
	print "(int $c $min $max)\n";
    }
    print "(alldifferent ", join(" ", @chars), ")\n";
    my $c = 0;
    my $maxcarry = 0;
    my $sum = pop(@words);
    while (1) {
	my @w = ();
	foreach my $w (@words) {
	    if (@{$w}) {
		push(@w, pop(@{$w}));
	    }
	}
	my $s = pop(@{$sum});
	last if @w == 0 && ! $s;
	my $c0 = "C" . ($c + 1);
	my @s = ($s);
	if (@w > 0) {
	    unshift(@s, "(* $base $c0)");
	    $_ = scalar(@w) * ($base - 1) + $maxcarry;
	    $maxcarry = int($_ / $base);
	    print "(int $c0 0 $maxcarry)\n";
	}
	my $c1 = "C$c";
	if ($c > 0) {
	    unshift(@w, $c1);
	}
	my $w = @w == 1 ? $w[0] : "(+ " . join(" ", @w) .")";
	my $s = @s == 1 ? $s[0] : "(+ " . join(" ", @s) .")";
	print "(= $w $s)\n";
	$c++;
    }
}
