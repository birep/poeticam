This app takes an image upload and returns a haiku,
using the Imagga api to generate annotations for the image.

This program contains publicly shared code from s3multifile
By Steve Saporta, license currently unknown,
and should not be used for any commercial purposes
until he responds to the license clarification request on github.

You must set environmental variables as follows:

AWS_ACCESS_KEY_ID=[your Access Key ID]
AWS_SECRET_ACCESS_KEY=[your Secret Access Key]
IMAGGA_API_KEY=[your Imagga Key]
IMAGGA_API_SECRET=[your Imagga secret]

And properly configure access rules for S3

Consult the documentation at https://github.com/sasaporta/s3multifile/blob/master/readme.md
for more info on S3 configuration.