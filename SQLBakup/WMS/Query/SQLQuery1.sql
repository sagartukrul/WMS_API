--select * from tbl_location;
select * from tblPOC_Pick where Req_Box_Qty !=0 and Delivery='0210829741'; 
--select Barcode, Mat_Code, Batch, Location from tblPOC_Stock where  Mat_Code='IN00731A';

--select * from tblPOC_Pick where Delivery= '0210829741' and Batch != '' and MatCode='1600517' and Batch ='23I170623';
--select * from tblPOC_Stock where Mat_Code='1600517' and Barcode = '1600517|23I170623|1466';

--select * from tblPOC_Import_Data  where Mat_Code='1600517' and Batch ='23I170623';

--update tblPOC_Stock set Status = 1 where Mat_Code='1600517'