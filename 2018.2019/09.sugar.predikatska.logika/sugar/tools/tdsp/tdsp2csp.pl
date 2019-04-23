#!/usr/bin/perl
##
## Converts Two-Dimensional Strip Packing Problem into Sugar CSP
##
## See Two-Dimensional Strip Packing web page in OR-Library
##     http://people.brunel.ac.uk/~mastjjb/jeb/orlib/stripinfo.html
##
## This program is a part of Sugar (a SAT-based Constraint Solver)
## software package.
##     http://bach.istc.kobe-u.ac.jp/sugar/
## (C) Naoyuki Tamura
##
use Getopt::Std;
use strict;
$| = 1;

use vars qw($opt_h $opt_m);

&getopts("hm");

if ($opt_h) {
    print "Usage: $0 file.2sp >file.csp\n";
    exit(1);
}
my $use_mul = $opt_m;

my ($width, $height, $area);
my @rect = ();

&read_2sp();
&write_csp();

exit 0;

sub read_2sp {
    ($width) = split(/\s+/, <>);
    if ($width <= 0) {
	die;
    }
    my ($n) = split(/\s+/, <>);
    if ($n <= 0) {
	die;
    }
    foreach my $i (1 .. $n) {
	my ($h, $w) = split(/\s+/, <>);
	if ($h <= 0 || $w <= 0) {
	    die;
	}
	$area += $h*$w;
	push(@rect, [$h, $w]);
    }
}

sub write_csp {
    print "; Two-Dimensional Strip Packing\n";
    my $lb = &lower_bound();
    my $ub = &upper_bound();
    print "(int width $width $width)\n";
    print "(int height $lb $ub)\n";
    print "(objective minimize height)\n";
    foreach my $i (0 .. @rect - 1) {
	my $x = "x$i";
	my $y = "y$i";
	my $r = "r$i";
	my ($h, $w) = @{$rect[$i]};
	my $wh = &wh($r, $w, $h);
	my $hw = &wh($r, $h, $w);
	print "(int $x 0 $width)\n";
	print "(int $y 0 $ub)\n";
	print "(int $r 0 1)\n";
	print "(<= (+ $x $wh) width)\n";
	print "(<= (+ $y $hw) height)\n";
    }
    foreach my $i (0 .. @rect - 1) {
	my $xi = "x$i";
	my $yi = "y$i";
	my $ri = "r$i";
	my ($hi, $wi) = @{$rect[$i]};
	my $whi = &wh($ri, $wi, $hi);
	my $hwi = &wh($ri, $hi, $wi);
	foreach my $j ($i + 1 .. @rect - 1) {
	    my $xj = "x$j";
	    my $yj = "y$j";
	    my $rj = "r$j";
	    my ($hj, $wj) = @{$rect[$j]};
	    my $whj = &wh($rj, $wj, $hj);
	    my $hwj = &wh($rj, $hj, $wj);
	    my $lrij = "lr${i}_${j}";
	    my $lrji = "lr${j}_${i}";
	    my $abij = "ab${i}_${j}";
	    my $abji = "ab${j}_${i}";
	    print "(bool $lrij)\n";
	    print "(bool $lrji)\n";
	    print "(bool $abij)\n";
	    print "(bool $abji)\n";
	    print "(or $lrij $lrji $abij $abji)\n";
	    print "(imp $lrij (<= (+ $xi $whi) $xj))\n";
	    print "(imp $lrji (<= (+ $xj $whj) $xi))\n";
	    print "(imp $abij (<= (+ $yi $hwi) $yj))\n";
	    print "(imp $abji (<= (+ $yj $hwj) $yi))\n";
	}
    }
    print "; END\n";
}

sub wh {
    my ($r, $x, $y) = @_;
    if ($use_mul) {
	return "(+ (* $x (- 1 $r)) (* $y $r))"
    } else {
	return "(if (= $r 0) $x $y)"
    }
}

sub lower_bound {
    my $h = ($area+$width-1) / $width;
    return int($h);
}

sub upper_bound {
    my @b = ();
    my $b = \@b;
    foreach my $i (0 .. @rect - 1) {
	my ($x0, $y0) = &find_place($i, $b);
	&place($i, $x0, $y0, $b);
    }
#    &show($b);
    return scalar(@b);
}

sub show {
    my ($b) = @_;
    my @c = (0 .. 9, "A" .. "Z", "a" .. "z");
    my $h = scalar(@{$b});
    foreach my $y (0 .. $h - 1) {
	foreach my $x (0 .. $width - 1) {
	    my $i = $b->[$y][$x];
	    if (defined $i) {
		print $c[$i % scalar(@c)];
	    } else {
		print ".";
	    }
	}
	print "\n";
    }
}

sub find_place {
    my ($i, $b) = @_;
    foreach my $y (0 .. scalar(@{$b})) {
	foreach my $x (0 .. $width-1) {
	    if (&can_place($i, $x, $y, $b)) {
		return ($x, $y);
	    }
	}
    }
    &show($b);
    die;
    return undef;
}

sub can_place {
    my ($i, $x0, $y0, $b) = @_;
    my ($h, $w) = @{$rect[$i]};
    if ($x0 + $w > $width) {
	return 0;
    }
    foreach my $y ($y0 .. $y0+$h-1) {
	if (! $b->[$y]) {
	    $b->[$y] = [];
	}
	foreach my $x ($x0 .. $x0+$w-1) {
	    if (defined $b->[$y][$x]) {
		return 0;
	    }
	}
    }
    return 1;
}

sub place {
    my ($i, $x0, $y0, $b) = @_;
    my ($h, $w) = @{$rect[$i]};
    foreach my $y ($y0 .. $y0+$h-1) {
	foreach my $x ($x0 .. $x0+$w-1) {
	    $b->[$y][$x] = $i;
	}
    }
}
