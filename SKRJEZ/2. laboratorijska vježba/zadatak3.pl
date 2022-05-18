#!/usr/bin/perl 

if(!@ARGV){
	while (<STDIN>){
		chomp($_);
		last if ($_ eq '.');
		push(@ARGV, $_);
	}	
}

foreach my $file (@ARGV) {
	print "\n";
	print "Datum: ";
	@a = split /\./, "$file";
	print "$a[1]\n";
	print "sat : broj pristupa\n";
	print "-------------------------------\n";
	
	open FILE, '<'.$file or die $!;
	$linija = $_;
	($sat) = $linija =~ m/[\d]{4}:([\d]{2}):[\d]{2}:[\d]{2}/;
	while(<FILE>) {
		if(m/[0-9]\/[A-Z][a-z]{2}\/[0-9]{4}\:[0-9][0-9]\:[0-9]{2}\:[0-9]{2}/){
			@f = split;
			@g = split /\:/, "@f";
			$rez{"@g[1]"} += 1;
		}
	}

	foreach $key (sort keys %rez){
		$value = $rez{$key};
		printf " $key : $value\n";
	}
	%rez = ();
}
