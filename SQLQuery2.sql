select Barcode, Mat_Code, Batch, Location from tblPOC_Stock where Mat_Code='1608857';

--select Barcode, Mat_Code, Batch, Location from tblPOC_Stock where Location!='' and Status=2;

--update tblPOC_Stock set Location = '', Status=1 where  Location='' and Status=3;



select * from tblPOC_Stock where Status = 3

update tblPOC_Stock set Location='', Status=3 where Barcode='1608857|11P170901|14076' and  Mat_Code = '1608857' and Batch = '11P170901' and Location!='';
