#!/usr/bin/perl
##
## Converts Golomb Ruler Problem into Sugar CSP
##
## See Golomb Ruler Problem web page in CSPLib
##     http://www.dcs.st-and.ac.uk/~ianm/CSPLib/prob/prob006/index.html
##
## This program is a part of Sugar (a SAT-based Constraint Solver)
## software package.
##     http://bach.istc.kobe-u.ac.jp/sugar/
## (C) Naoyuki Tamura
##
#
# -m	-l
# 1 	0
# 2 	1
# 3 	3
# 4 	6
# 5 	11
# 6 	17
# 7 	25
# 8 	34
# 9 	44
# 10 	55
# 11 	72
# 12 	85
# 13 	106
# 14 	127
# 15 	151
# 16 	177
# 17 	199
# 18 	216
# 19 	246
# 20 	283
# 21 	333
# 22 	356
# 23 	372
#
# ./golombRuler.pl -m 8 >csp/golomb-8.csp
# ./golombRuler.pl -m 10 -l 55 >csp/golomb-10-55.csp
#
use Getopt::Std;
use strict;
$| = 1;

use vars qw($opt_h $opt_m $opt_l);

&getopts("hm:l:");
my $marks = $opt_m;
my $length = $opt_l;

if ($opt_h || $marks <= 0) {
    print "Usage: $0 -m marks [-l length] >file.csp\n";
    exit(1);
}

my @d = ();

print "; Golomb ruler of $marks marks";
if ($length) {
    print " for length $length";
}
print "\n";
&write_csp();
print "; END\n";
exit 0;

sub write_csp {
    my ($lb, $ub);
    if ($length) {
	$lb = $length;
	$ub = $length;
	print "(int length $lb $ub)\n";
    } else {
	$lb = &lower_bound();
	$ub = &upper_bound();
	print "(int length $lb $ub)\n";
	print "(objective minimize length)\n";
    }
    foreach my $i (0 .. $marks-1) {
	if ($i == 0) {
	    &mark($i, 0, 0);
	} else {
	    &mark($i, 0, $ub);
	}
    }
    foreach my $i (0 .. $marks-1) {
	my $v1 = "m_${i}";
	if ($i < $marks-1) {
	    my $v2 =  "m_" . ($i+1);
	    print "(< $v1 $v2)\n";
	} else {
	    print "(<= $v1 length)\n";
	}
    }
    @_ = ();
    foreach my $i (0 .. $marks-1) {
	foreach my $j ($i+1 .. $marks-1) {
	    if (1) {
		my $d = "d_${j}_${i}";
		print "(int $d 0 $ub)\n";
		print "(= $d (- m_${j} m_${i}))\n";
		push(@_, $d);
	    } else {
		push(@_, "(- m_${j} m_${i})");
	    }
	}
    }
    print "(alldifferent ", join(" ", @_), ")\n";
}

sub mark {
    my ($i, $lo, $hi) = @_;
    print "(int m_${i} $lo $hi)\n";
}

sub lower_bound {
    return $marks*($marks-1)/2;
}

sub upper_bound {
    return (1 << ($marks-1)) - 1;
}
