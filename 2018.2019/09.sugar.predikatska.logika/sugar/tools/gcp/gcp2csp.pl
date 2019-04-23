#!/usr/bin/perl
##
## Converts Graph Coloring Problem into Sugar CSP
##
## See Graph Coloring Problem web page in OR-Library
##     http://people.brunel.ac.uk/~mastjjb/jeb/orlib/colourinfo.html
##
## This program is a part of Sugar (a SAT-based Constraint Solver)
## software package.
##     http://bach.istc.kobe-u.ac.jp/sugar/
## (C) Naoyuki Tamura
##
use Getopt::Std;
use strict;
$| = 1;

use vars qw($opt_h $opt_n);

&getopts("hn");
my $in = shift(@ARGV);

if ($opt_h) {
    print "Usage: $0 file.col >file.csp\n";
    exit(1);
}

my ($nodes, $edges);
my @node = ();
my %edge = ();

&read_gcp();
print "; Graph Coloring Problem\n";
&write_csp();
print "; END\n";
exit 0;

sub read_gcp {
    if ($in =~ /\.gz$/) {
	open(IN, "gzip -dc $in |") || die;
    } else {
	open(IN, "<$in") || die;
    }
    while (<IN>) {
	chomp;
	if (/^\s*$/ || /^\s*c/) {
	    next;
	}
	if (/^\s*p\s+/) {
	    if (/^\s*p\s+\S+\s+(\d+)\s+(\d+)\s*$/) {
		($nodes, $edges) = ($1, $2);
	    } else {
		die $_;
	    }
	} elsif (/^\s*e\s+/) {
	    if (/^\s*e\s+(\d+)\s+(\d+)\s*$/) {
		$edge{$1}{$2} = 1;
		$edge{$2}{$1} = 1;
	    } else {
		die $_;
	    }
	} else {
	    die $_;
	}
    }
    close(IN);
    @node = sort {$a <=> $b} keys %edge;
    if ($nodes != scalar(@node)) {
	$_ = scalar(@node);
	warn "Node size $nodes != $_";
    }
}

sub write_csp {
    my $lb = &lower_bound();
    my $ub = &upper_bound();
    print "(int color $lb $ub)\n";
    print "(objective minimize color)\n";
    foreach my $node (@node) {
	my $n = "n$node";
	print "(int $n 1 $ub)\n";
	print "(<= $n color)\n";
    }
    foreach my $node (@node) {
	foreach my $node1 (sort { $a <=> $b} keys %{$edge{$node}}) {
	    if ($node <= $node1) {
		my $n = "n$node";
		my $n1 = "n$node1";
		print "(!= $n $n1)\n";
	    }
	}
    }
}

sub lower_bound {
    return 2;
}

sub upper_bound {
    my %color = ();
    my $color = 0;
    foreach my $node (@node) {
	my %c = ();
#	print "$node <-->";
	foreach my $node1 (sort { $a <=> $b} keys %{$edge{$node}}) {
#	    print " $node1=$color{$node1}";
	    if ($color{$node1}) {
		$c{$color{$node1}} = 1;
	    }
	}
#	print "\n";
	my $c;
	foreach (1 .. $color) {
	    if (! $c{$_}) {
		$c = $_;
		last;
	    }
	}
	if (! $c) {
	    $color++;
	    $c = $color;
	}
	$color{$node} = $c;
#	print "$node $c\n";
    }
    return $color;
}
