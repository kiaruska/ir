C=javac 

J=java -Xmx2G

all: c_annotation

c_annotation:
	$C TweetAnnotation.java
	$C TweetFilter.java

annotation:
	$J TweetAnnotation

