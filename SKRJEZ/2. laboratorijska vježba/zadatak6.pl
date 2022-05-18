#!/usr/bin/perl

if(!@ARGV){
	while (<STDIN>){
		chomp($_);
		last if ($_ eq '.');
		push(@ARGV, $_);
	}	
}

sub racunaj {
	#print "Pozvan\n";
	#$a = "$_[0]" . "$_[0]";
	$o = ord(uc($_[0]));
	$p = ord(uc($_[1]));

	#print "$o $p\n";

	$a = ($o + $p) % 26;
	#print "$a";
	$b = chr(65 + $a);
}
$op = $ARGV[0];
shift @ARGV;
while (defined($line = <>)) {
	foreach $p (split //, $line) {
		if(ord($p) == 32){
			$rez = $rez . ' ';
			next;
		}
		if(ord($p) == 10){
			$rez = $rez . ' ';
			next;
		}
		$k =  &racunaj($p,$op);
		$rez = $rez . $k;
		#join '', $rez, $k;
		#print "$p\n";
	}

	print "$rez\n";
	$rez = '';
}
#print "\n";

#foreach $i (@alphabet){
	#print "$i\n";
#}

#print "$f";

=pod
$n = &racunaj(e);
print "$a";
print (ord(Z));
print "\n";
print $alphabet[0];

=cut