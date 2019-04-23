#!/usr/bin/perl
##
## Converts BIBD into Sugar CSP
##
## See BIBD web page in CSPLib
##     http://www.dcs.st-and.ac.uk/~ianm/CSPLib/prob/prob028/index.html
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

my ($v, $b, $r, $k, $lambda);
$v = shift(@ARGV);
$k = shift(@ARGV);
$lambda = shift(@ARGV);

if ($opt_h || ! $v || ! $k || ! $lambda) {
    print "Usage: $0 v k lambda >file.csp\n";
    print "Examples\n";
    print "\tv= 7 k=3 lambda=1 (b= 7 r=3)\n";
    print "\tv=15 k=3 lambda=1 (b=35 r=7) # Kirkman's School Girl Problem\n";
    print "\tv=16 k=4 lambda=1 (b=20 r=5) # 5 mahjongg games at 4 tables\n";
    exit(1);
}

$r = $lambda * ($v - 1) / ($k - 1);
$b = $v * $r / $k;
if ($r != int($r) || $b != int($b)) {
    die "Illegal paramemter v=$v k=$k lambda=$lambda";
}

print "; BIBD v=$v b=$b r=$r k=$k lambda=$lambda\n";
&write_csp();
print "; END\n";
exit 0;

sub write_csp {
    foreach my $i (1 .. $v) {
	foreach my $j (1 .. $b) {
	    my $x = "x_${i}_${j}";
	    print "(int $x 0 1)\n";
	}
    }
    foreach my $i (1 .. $v) {
	my @s = ();
	foreach my $j (1 .. $b) {
	    my $x = "x_${i}_${j}";
	    push(@s, $x);
	}
	print "(= (+ ", join(" ", @s), ") $r)\n";
    }
    foreach my $j (1 .. $b) {
	my @s = ();
	foreach my $i (1 .. $v) {
	    my $x = "x_${i}_${j}";
	    push(@s, $x);
	}
	print "(= (+ ", join(" ", @s), ") $k)\n";
    }
    foreach my $i1 (1 .. $v) {
	foreach my $i2 ($i1+1 .. $v) {
	    my @s = ();
	    foreach my $j (1 .. $b) {
		my $x1 = "x_${i1}_${j}";
		my $x2 = "x_${i2}_${j}";
		push(@s, "(min $x1 $x2)");
	    }
	    print "(= (+ ", join(" ", @s), ") $lambda)\n";
	}
    }
}
