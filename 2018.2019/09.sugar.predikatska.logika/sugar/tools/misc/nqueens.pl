#!/usr/bin/perl
##
## Converts N-Queens Problem into Sugar CSP
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

if ($opt_h || $n < 4) {
    print "Usage: $0 n >file.csp\n";
    exit(1);
}

print "; $n-Queens Problem\n";
&write_csp();
print "; END\n";
exit 0;

sub write_csp {
    foreach my $i (1 .. $n) {
	my $q = "q_${i}";
	print "(int $q 1 $n)\n";
    }
    @_ = ();
    foreach my $i (1 .. $n) {
	my $q = "q_${i}";
	push(@_, $q);
    }
    print "(alldifferent ", join(" ", @_), ")\n";
    @_ = ();
    foreach my $i (1 .. $n) {
	my $q = "q_${i}";
	push(@_, "(+ $q $i)");
    }
    print "(alldifferent ", join(" ", @_), ")\n";
    @_ = ();
    foreach my $i (1 .. $n) {
	my $q = "q_${i}";
	push(@_, "(- $q $i)");
    }
    print "(alldifferent ", join(" ", @_), ")\n";
}
