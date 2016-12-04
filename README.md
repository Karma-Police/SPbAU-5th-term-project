# SPbAU-5th-term-project
SPbAU 5th term project on bioinformatics

<h3> How to use? </h3>
<p> Run madTester.py (Python 3 is required) with "data list" as first argument. You can also provide an output directory as the second argument. </p>
```
python3 ./madTester.py [PATH TO DATA_LIST FILE] [(optional)PATH_TO_OUTPUT_DIR]
```
<h3> Data_list format </h3>
<p> The data_list file consists of several tests. Each test is given is described by exactly 5 lines:</p>
<ol>
<li/> Name of the test <pre># mus_musculus</pre>
<li/> Path to reference genome <pre> ref: /mydata/genome/refgenome.fa</pre>
<li/> Path to gtf file <pre>gtf: /mydata/genome/gtffile.gtf</pre>
<li/> Path to left reads separated by &amp; <pre>r1: /mydata/genome/reads1-1.fastq&amp;/mydata/genome/reads2-1.fastq</pre>
<li/> Path to right reads separated by &amp; <pre>r2: /mydata/genome/reads1-2.fastq&amp;/mydata/genome/reads2-2.fastq</pre>
</ol>
<p>Check the example in "scripts" directory.</p>
