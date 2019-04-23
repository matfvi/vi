#!/usr/bin/perl
##
## Converts Job-shop Scheduling Problem into Sugar CSP
##
## See Job-shop scheduling web page in OR-Library
##     http://people.brunel.ac.uk/~mastjjb/jeb/orlib/jobshopinfo.html
##
## This program is a part of Sugar (a SAT-based Constraint Solver)
## software package.
##     http://bach.istc.kobe-u.ac.jp/sugar/
## (C) Naoyuki Tamura
##
use Getopt::Std;
use strict;
$| = 1;

use vars qw($opt_h $opt_b $opt_x $opt_m);

&getopts("hbxm:");
my $in = shift(@ARGV);

if ($opt_h) {
    print "Usage: $0 file.jss >file.csp\n";
    exit(1);
}

my $bool = $opt_b;
my $exclusive = $opt_x;
my $makespan = $opt_m;

my ($jobs, $machines);
my @j_m = ();
my @j_p = ();
my @m_j = ();
my @m_p = ();

&read_jss();
&write_csp();

exit 0;

sub read_jss {
    open(IN, "<$in") || die;
    chomp($_ = <IN>);
    ($jobs, $machines) = split;
    @j_m = ();
    @j_p = ();
    foreach my $i (0.. $jobs-1) {
	chomp($_ = <IN>);
	@_ = split;
	$j_m[$i] = [];
	$j_p[$i] = [];
	foreach my $j (0.. $machines-1) {
	    $j_m[$i]->[$j] = shift(@_);
	    $j_p[$i]->[$j] = shift(@_);
	}
    }
    close(IN);
    @m_j = ();
    @m_p = ();
    foreach my $i (0.. $jobs-1) {
	foreach my $j (0.. $machines-1) {
	    my $m = $j_m[$i][$j];
	    if (! $m_j[$m]) {
		$m_j[$m] = [];
	    }
	    if (! $m_p[$m]) {
		$m_p[$m] = [];
	    }
	    $m_j[$m][$i] = $j;
	    $m_p[$m][$i] = $j_p[$i][$j];
	}
    }
}

sub write_csp {
    print "; JSS\n";
    print "; $jobs $machines\n";
    foreach my $i (0.. $jobs-1) {
	@_ = ();
	foreach my $j (0.. $machines-1) {
	    $_ = $j_m[$i]->[$j] . " " . $j_p[$i]->[$j];
	    push(@_, $_);
	}
	print "; ", join(" ", @_), "\n";
    }
    my $lb = &lower_bound();
    my $ub = &upper_bound();
    print "(int makespan $lb $ub)\n";
    if ($makespan) {
	print "(<= makespan $makespan)\n";
    } else {
	print "(objective minimize makespan)\n";
    }
    foreach my $i (0 .. $jobs-1) {
	foreach my $j (0 .. $machines-1) {
	    my $s = "s_${i}_${j}";
	    print "(int $s 0 $ub)\n";
	}
    }
    foreach my $i (0 .. $jobs-1) {
	foreach my $j (0 .. $machines-1) {
	    my $j1 = $j + 1;
	    my $s = "s_${i}_${j}";
	    my $s1 = "s_${i}_${j1}";
	    if ($j1 >= $machines) {
		$s1 = "makespan";
	    }
	    my $p = $j_p[$i]->[$j];
	    print "(<= (+ $s $p) $s1)\n";
	}
    }
    foreach my $m (0 .. $machines-1) {
	foreach my $i0 (0 .. $jobs-1) {
	    foreach my $i1 ($i0+1 .. $jobs-1) {
		my $j0 = $m_j[$m][$i0];
		my $j1 = $m_j[$m][$i1];
		my $s0 = "s_${i0}_${j0}";
		my $s1 = "s_${i1}_${j1}";
		my $p0 = $j_p[$i0][$j0];
		my $p1 = $j_p[$i1][$j1];
		if ($bool) {
		    my $p01 = "p_${i0}_${j0}_${j1}";
		    print "(bool $p12)\n";
		    my $p10 = "p_${i0}_${j1}_${j0}";
		    if ($exclusive) {
			$p10 = "(! $p01)";
		    } else {
			print "(bool $p10)\n";
			print "(or $p01 $p10)\n";
		    }
		    print "(imp $p01 (<= (+ $s0 $p0) $s1))\n";
		    print "(imp $p10 (<= (+ $s1 $p1) $s0))\n";
		} else {
		    print "(or (<= (+ $s0 $p0) $s1) (<= (+ $s1 $p1) $s0))\n";
		}
	    }
	}
    }
}

sub lower_bound {
    my $x;
    foreach my $i (0 .. $jobs-1) {
	my $s = 0;
	foreach my $j (0 .. $machines-1) {
	    $s += $j_p[$i][$j];
	}
#	print "job $i $s\n";
	if (! $x || $x < $s) {
	    $x = $s;
	}
    }
    foreach my $j (0 .. $machines-1) {
	my $s = 0;
	foreach my $i (0 .. $jobs-1) {
	    $s += $m_p[$j][$i];
	}
#	print "machine $j $s\n";
	if (! $x || $x < $s) {
	    $x = $s;
	}
    }
    return $x;
}

sub upper_bound {
    my $s = 0;
    my $cmd = "java -cp .:cream105.jar JSSP <$in";
    chomp($s = `$cmd`);
    return $s;
}
