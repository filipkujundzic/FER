#!/usr/bin/perl

$first = <>;
@p = split(";",$first);

while ($line = <>) {
	$tmp = 0;
	next if $. < 2;
	@s = split(";",$line);

	$sum = 0;

	foreach $i (3,4,5,6,7,8,9){
		next if $s[$i] == "-";
		$sum += "$s[$i]" * "$p[$i-3]";

	}
	$rez{"$s[$tmp+1], $s[$tmp+2] ($s[$tmp])"} = $sum;
	$tmp += 1;
}

while (($key, $value) = each %rez){
	$rez2{$value}=$key;
}

%rez=%rez2;

print "\n";
print "Lista po rangu:\n";
print "------------------\n";

$z = 1;
foreach $key (reverse sort keys %rez2){
	$value = $rez2{$key};
	printf "%3d. %-40s : %-3.2f\n",$z,$value,$key;
	$z++;
}