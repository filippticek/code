#!/usr/bin/perl

while (defined($redak = <>)){
	chomp;
	if (defined $file && $file ne $ARGV) {
		foreach (0..23) {
			printf " %02d : %d\n", $_, shift(@sati);
		}
	}
	if (! defined $file || $file ne $ARGV && $ARGV ne "-") {
		$file = $ARGV;
		@temp = split /\./, $ARGV;
		print "\n Datum: $temp[1]\n";
		print " sat : broj pristupa\n";
		print "-------------------------------\n";
		foreach (0..23) {
			push @sati , 0;
		}
	}
	if ($file eq $ARGV || $ARGV eq "-") {
		@temp = split /:/, $redak;
		$sati[$temp[1]] += 1;
	}
}
foreach (0..23) {
	printf " %02d : %d\n", $_, shift(@sati);
}
