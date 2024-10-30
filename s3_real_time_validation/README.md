# AUTOMATING AWS WITH PYTHON | PART 6 : S3 REAL TIME VALIDATION

![Picture1](https://github.com/user-attachments/assets/01f9eaa9-b6f4-40e2-9067-007fc479c167)

Today we will setup a Lambda function which will be triggered whenever a new CSV file is uploaded to an S3 bucket. 
It will then validate the file and if any discrepancies are found, it will move the file to an “error” bucket.

## I.	Create a Lambda function:

•	Go to the AWS console, Lambda, and create a Lambda function

•	Choose "Author from scratch". 

•	In the Function name field, enter BillingBucketParser. 

•	For the Runtime, select Python 3.12

## II.	Create two S3 buckets

•	Create two S3 buckets, one for uploading csv files and other for error files.

•	touch s3_buckets.py

•	Paste into it the code from the GitHub repository.

•	Run: python s3_buckets.py

## III.	Create three files in VS code:

•	touch lambda_function.py template.yaml event.json

•	Paste into them the codes from the GitHub repository.

•	Run: python lambda_function.py

## IV.	File upload

•	Upload to the bucket named “dct-billing-st” the provided csv file named “billing_data_dairy_may_2023”

## V.	Check the operation manually

•	On VS Code run with command prompt: sam local invoke -e event.json
        *You need to have docker installed and running 

![Picture2](https://github.com/user-attachments/assets/5fe453a3-e2ae-4fa2-86e9-ff49adb16b1a)

•	Now you can see the results. Since an error was fond in the date format, this file was moved into the error bucket, 
  and the original file that was in the first bucket was delete.

•	Check it out in the S3 buckets on the AWS console.

## VI.	Create a zip file

•	Go to powershell and run: “Compress-Archive -Path lambda_function.py -DestinationPath lambda_function.zip”

## VII.	Update the Lambda function permissions

•	touch update_policies.py

•	Paste into it the code from the GitHub repository.

•	Run: python update_policies.py

## VIII.	Increase Lambda function timeout

Create a new file:

•	touch increase_lambda_timeout.py

•	Paste into it the code from the GitHub repository.

•	Run: python increase_lambda_timeout.py

## IX.	Add a trigger to the Lambda function

Create a new file:

•	touch lambda_trigger.py

•	Paste into it the code from the GitHub repository.

•	Run: python lambda_trigger.py

## X.	Update the Lambda function 

•	touch update_lambda_function.py

•	Paste into it the code from the GitHub repository.

•	Run: python update_lambda_function.py

## XI.	Test it out

Upload the “billing_data_meat_may_2023” file into the “dct-billing.st” bucket

It should be moved into “dct-billing-errors-st” bucket automatically.



