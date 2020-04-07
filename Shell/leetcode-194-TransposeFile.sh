#!/usr/bin/env bash

##194. Transpose File
#Given a text file file.txt, transpose its content.
#
#You may assume that each row has the same number of columns and each field is separated by the ' ' character.
#
#Example:
#
#If file.txt has the following content:
#
#name age
#alice 21
#ryan 30
#Output the following:
#
#name alice ryan
#age 21 30

#194. 转置文件
#给定一个文件 file.txt，转置它的内容。
#
#你可以假设每行列数相同，并且每个字段由 ' ' 分隔.
#
#示例:
#
#假设 file.txt 文件内容如下：
#
#name age
#alice 21
#ryan 30
#应当输出：
#
#name alice ryan
#age 21 30

# Read from the file file.txt and print its transposed content to stdout.
column=$(awk '{print NF}' file.txt | uniq)
for((i=1;i<=column;i++))
do
  cut -d' ' -f$i file.txt|xargs
done