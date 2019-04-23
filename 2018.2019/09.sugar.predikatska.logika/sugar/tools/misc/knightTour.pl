#!/usr/bin/perl
##
## Converts Knight's Tour Problem into Sugar CSP
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
print "; Knight's Tour $n x $n\n";
&write_csp();
print "; END\n";
exit 0;

sub write_csp {
    my @d = ([-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]);
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
	foreach my $j (1 .. $n) {
	    my $x = "x_${i}_${j}";
	    @_ = ();
	    push(@_, "(= $x $n2)");
	    foreach (@d) {
		my ($di,$dj) = @{$_};
		my $i1 = $i + $di;
		my $j1 = $j + $dj;
		if (1 <= $i1 && $i1 <= $n && 1 <= $j1 && $j1 <= $n) {
		    my $x1 = "x_${i1}_${j1}";
		    push(@_, "(= (+ $x 1) $x1)");
		}
	    }
	    print "(or ", join(" ", @_), ")\n";
	}
    }
}
