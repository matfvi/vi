#!/usr/bin/perl
##
## Converts Social Golfer Problem into Sugar CSP
##
## See Social Golfer Problem web page in CSPLib
##     http://www.dcs.st-and.ac.uk/~ianm/CSPLib/prob/prob010/index.html
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

my ($groups, $members, $weeks);
$groups = shift(@ARGV);
$members = shift(@ARGV);
$weeks = shift(@ARGV);

if ($opt_h || ! $groups || ! $members || ! $weeks) {
    print "Usage: $0 groups members groups >file.csp\n";
    print "Examples\n";
    print "\t$0 3 2 5\n";
    print "\t$0 6 3 7\n";
    print "\t$0 8 4 9\n";
    exit(1);
}

print "; Social Golfer Problem: $groups groups, $members members, $weeks weeks\n";
&write_csp();
print "; END\n";
exit 0;

sub write_csp {
    my $v = $groups * $members;
    my $b = $weeks * $groups;
    foreach my $i (1 .. $v) {
	foreach my $j (1 .. $b) {
	    my $x = "x_${i}_${j}";
	    print "(int $x 0 1)\n";
	}
    }
    foreach my $i (1 .. $v) {
	foreach my $w (1 .. $weeks) {
	    my @s = ();
	    my $j = ($w - 1)*$groups + 1;
	    foreach (1 .. $groups) {
		my $x = "x_${i}_${j}";
		push(@s, $x);
		$j++;
	    }
	    print "(= (+ ", join(" ", @s), ") 1)\n";
	}
    }
    foreach my $j (1 .. $b) {
	my @s = ();
	foreach my $i (1 .. $v) {
	    my $x = "x_${i}_${j}";
	    push(@s, $x);
	}
	print "(= (+ ", join(" ", @s), ") $members)\n";
    }
    foreach my $i1 (1 .. $v) {
	foreach my $i2 ($i1+1 .. $v) {
	    my @s = ();
	    foreach my $j (1 .. $b) {
		my $x1 = "x_${i1}_${j}";
		my $x2 = "x_${i2}_${j}";
		push(@s, "(min $x1 $x2)");
	    }
	    print "(<= (+ ", join(" ", @s), ") 1)\n";
	}
    }
}
