#!/usr/bin/perl
##
## Converts Magic Square Problem into Sugar CSP
##
## See Magic Squares web page in CSPLib
##     http://www.dcs.st-and.ac.uk/~ianm/CSPLib/prob/prob019/spec.html
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
my $n = shift(@ARGV);

if ($opt_h || $n < 3) {
    print "Usage: $0 n >file.csp\n";
    exit(1);
}

my $n2 = $n * $n;
my $sum = $n * ($n2 + 1) / 2;

print "; Magic Square $n x $n\n";
&write_csp();
print "; END\n";
exit 0;

sub write_csp {
    @_ = ();
    foreach my $i (1 .. $n) {
	foreach my $j (1 .. $n) {
	    my $x = "x_${i}_${j}";
	    push(@_, $x);
	    print "(int $x 1 $n2)\n";
	}
    }
    print "(alldifferent ", join(" ", @_), ")\n";
    foreach my $i (1 .. $n) {
	@_ = ();
	foreach my $j (1 .. $n) {
	    my $x = "x_${i}_${j}";
	    push(@_, $x);
	}
	print "(= (+ ", join(" ", @_), ") $sum)\n";
    }
    foreach my $j (1 .. $n) {
	@_ = ();
	foreach my $i (1 .. $n) {
	    my $x = "x_${i}_${j}";
	    push(@_, $x);
	}
	print "(= (+ ", join(" ", @_), ") $sum)\n";
    }
    @_ = ();
    foreach my $i (1 .. $n) {
	my $j = $i;
	my $x = "x_${i}_${j}";
	push(@_, $x);
    }
    print "(= (+ ", join(" ", @_), ") $sum)\n";
    @_ = ();
    foreach my $i (1 .. $n) {
	my $j = $n - $i + 1;
	my $x = "x_${i}_${j}";
	push(@_, $x);
    }
    print "(= (+ ", join(" ", @_), ") $sum)\n";
}
