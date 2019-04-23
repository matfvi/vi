#!/usr/bin/perl
##
## Converts Open-shop Scheduling Problem into Sugar CSP
##
## See Open-shop scheduling web page in OR-Library
##     http://people.brunel.ac.uk/~mastjjb/jeb/orlib/openshopinfo.html
##
## This program is a part of Sugar (a SAT-based Constraint Solver)
## software package.
##     http://bach.istc.kobe-u.ac.jp/sugar/
## (C) Naoyuki Tamura
##
use Getopt::Std;
use strict;
$| = 1;

use vars qw($opt_h $opt_c $opt_b $opt_x $opt_m);

&getopts("hcbxm:");

if ($opt_h) {
    print "Usage: $0 file.oss >file.csp\n";
    exit(1);
}

my $n;
my @pt = ();
my $cumulative = $opt_c;
my $bool = $opt_b;
my $exclusive = $opt_x;
my $makespan = $opt_m;

&read_oss();
&write_csp();

exit 0;

sub read_oss {
    chomp($_ = <>);
    @_ = split;
    @pt = ();
    if (@_ == 2 && $_[0] == $_[1]) {
	$n = $_[0];
	while (<>) {
	    tr/\r\n//d;
	    @_ = split;
	    my $m = shift(@_);
	    if ($m == 0) {
		last;
	    }
	    my @s = ();
	    while (@_) {
		my $i = shift(@_);
		$s[$i] = shift(@_);
	    }
	    if ($m != $n || @s != $n) {
		@pt = ();
		last;
	    }
	    push(@pt, \@s);
	}
	if (@pt != $n) {
	    @pt = ();
	}
    }
    if (@pt == 0) {
	print "; ERROR : read format error\n";
    }
}

sub write_csp {
    print "; OSS\n";
    print "; $n $n\n";
    foreach (@pt) {
	print "; ", join(" ", @{$_}), "\n";
    }
    my $lb = &lower_bound();
    my $ub = &upper_bound();
    print "(int makespan $lb $ub)\n";
    if ($makespan) {
	print "(<= makespan $makespan)\n";
    } else {
	print "(objective minimize makespan)\n";
    }
    foreach my $j (0 .. $n-1) {
	foreach my $m (0 .. $n-1) {
	    my $s = "s_${j}_${m}";
	    my $p = $pt[$j]->[$m];
	    print "(int $s 0 $ub)\n";
	    print "(<= (+ $s $p) makespan)\n";
	}
    }
    if ($cumulative) {
	foreach my $j (0 .. $n-1) {
	    my @c;
	    foreach my $m (0 .. $n-1) {
		my $s = "s_${j}_${m}";
		my $p = $pt[$j]->[$m];
		push(@c, "($s $p nil 1)");
	    }
	    my $c = join(" ", @c);
	    print "(cumulative ($c) 1)\n";
	}
	foreach my $m (0 .. $n-1) {
	    my @c;
	    foreach my $j (0 .. $n-1) {
		my $s = "s_${j}_${m}";
		my $p = $pt[$j]->[$m];
		push(@c, "($s $p nil 1)");
	    }
	    my $c = join(" ", @c);
	    print "(cumulative ($c) 1)\n";
	}
    } else {
	foreach my $j (0 .. $n-1) {
	    foreach my $m (0 .. $n-1) {
		my $s1 = "s_${j}_${m}";
		my $p1 = $pt[$j]->[$m];
		foreach my $k ($m+1 .. $n-1) {
		    my $s2= "s_${j}_${k}";
		    my $p2 = $pt[$j]->[$k];
		    if ($bool) {
			my $p12 = "p_${j}_${m}_${k}";
			print "(bool $p12)\n";
			my $p21 = "p_${j}_${k}_${m}";
			if ($exclusive) {
			    $p21 = "(! $p12)";
			} else {
			    print "(bool $p21)\n";
			    print "(or $p12 $p21)\n";
			}
			print "(imp $p12 (<= (+ $s1 $p1) $s2))\n";
			print "(imp $p21 (<= (+ $s2 $p2) $s1))\n";
		    } else {
			print "(or (<= (+ $s1 $p1) $s2) (<= (+ $s2 $p2) $s1))\n";
		    }
		}
	    }
	}
	foreach my $m (0 .. $n-1) {
	    foreach my $j (0 .. $n-1) {
		my $s1 = "s_${j}_${m}";
		my $p1 = $pt[$j]->[$m];
		foreach my $k ($j+1 .. $n-1) {
		    my $s2= "s_${k}_${m}";
		    my $p2 = $pt[$k]->[$m];
		    if ($bool) {
			my $p12 = "q_${m}_${j}_${k}";
			print "(bool $p12)\n";
			my $p21 = "q_${m}_${k}_${j}";
			if ($exclusive) {
			    $p21 = "(! $p12)";
			} else {
			    print "(bool $p21)\n";
			    print "(or $p12 $p21)\n";
			}
			print "(imp $p12 (<= (+ $s1 $p1) $s2))\n";
			print "(imp $p21 (<= (+ $s2 $p2) $s1))\n";
		    } else {
			print "(or (<= (+ $s1 $p1) $s2) (<= (+ $s2 $p2) $s1))\n";
		    }
		}
	    }
	}
    }
    print "; END\n";
}

sub lower_bound {
    my $x;
    foreach my $i (0 .. $n - 1) {
	my $s = 0;
	foreach my $j (0 .. $n - 1) {
	    $s += $pt[$i][$j];
	}
	if (! $x || $x < $s) {
	    $x = $s;
	}
    }
    foreach my $j (0 .. $n - 1) {
	my $s = 0;
	foreach my $i (0 .. $n - 1) {
	    $s += $pt[$i][$j];
	}
	if (! $x || $x < $s) {
	    $x = $s;
	}
    }
    return $x;
}

sub upper_bound {
    my $s = 0;
    foreach my $k (0 .. $n - 1) {
	my $x = 0;
	foreach my $i (0 .. $n - 1) {
	    my $j = ($i + $k) % $n;
	    if (! $x || $x < $pt[$i][$j]) {
		$x = $pt[$i][$j];
	    }
	}
	$s += $x;
    }
    return $s;
}
