xassets_script
==============

This script organise assets as per iOS xassets catalog structure 
Folder name contain Images (1x - 2x - 3x) and Contents.json

Json format supported :

{
  "images" : [
    {
      "idiom" : "iphone",
      "scale" : "1x",
      "filename" : "image.png"
    },
    {
      "idiom" : "iphone",
      "scale" : "2x",
      "filename" : "image@2x.png"
    },
    {
      "idiom" : "iphone",
      "subtype" : "retina4",
      "scale" : "2x"
    },
    {
      "idiom" : "iphone",
      "scale" : "3x"
    }
  ],
  "info" : {
    "version" : 1,
    "author" : "xcode"
  }
}
