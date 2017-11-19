==================================================================

Dataset: YFCC100M

Yahoo! Flickr Creative Commons 100M
A dataset of 100 million public Flickr photos/videos
http://bit.ly/yfcc100md

==================================================================

Yahoo! Webscope ReadMe

The data included herein is provided as part of the Yahoo! Webscope program for use solely under the terms of a signed Yahoo! Data Sharing Agreement.

Any publication using this data should attribute Yahoo!, ideally in the bibliography of the paper, unless Yahoo! explicitly requests no attribution. Please include the phrase Yahoo! Webscope, the web address http://research.yahoo.com/Academic_Relations and the name of the specific dataset used, including version number if applicable. For example:

Yahoo! Webscope dataset YFCC100M
[http://labs.yahoo.com/Academic_Relations]

Please send a copy of each paper and its full citation information to research-data-requests@yahoo-inc.com upon publication.

This data may be used only for academic research purposes and may not be used for any commercial purposes, by any commercial entity, or by any party not under a signed Data Sharing Agreement. The data may not be reproduced in whole or in part, may not be posted on the web, on internal networks, or in networked data stores, and may not be archived offsite. The data must be returned to Yahoo! at the end of the research project or in three years, whichever comes first.

This dataset was produced from Yahoo!'s records and has been reviewed by an internal board to assure that no personally identifiable information is revealed.  You may not perform any analysis, reverse engineering or processing of the data or any correlation with other data sources that could be used to determine or infer personally identifiable information.

Please refer to the Data Sharing Agreement for complete terms. Contact research-data-requests@yahoo-inc.com with questions.

==================================================================


+++ Full Description +++

This dataset contains a list of photos and videos. This list is compiled from data available on Yahoo! Flickr. All the photos and videos provided in the list are licensed under one of the Creative Commons copyright licenses, and as such they can be used for benchmarking purposes as long as the photographer/videographer is credited for the original creation. In particular, the data in this dataset was made available under one of the following licenses:

   * [[http://creativecommons.org/licenses/by-nc/2.0/][Attribution-NonCommercial License]]
   * [[http://creativecommons.org/licenses/by-nc-sa/2.0/][Attribution-NonCommercial-ShareAlike License]]
   * [[http://creativecommons.org/licenses/by-nc-nd/2.0/][Attribution-NonCommercial-NoDerivs License]]
   * [[http://creativecommons.org/licenses/by/2.0/][Attribution License]]
   * [[http://creativecommons.org/licenses/by-sa/2.0/][Attribution-ShareAlike License]]
   * [[http://creativecommons.org/licenses/by-nd/2.0/][Attribution-NoDerivs License]]

This dataset is formed by ten bzip2-compressed files (yfcc100m_dataset-0.bz2 to yfcc100m_dataset-9.bz2), each holding 10M lines, where each lines contains the following tab-separated fields:
   * Photo/video identifier
   * User NSID
   * User nickname
   * Date taken
   * Date uploaded
   * Capture device
   * Title
   * Description
   * User tags (comma-separated)
   * Machine tags (comma-separated)
   * Longitude
   * Latitude
   * Accuracy
   * Photo/video page URL
   * Photo/video download URL
   * License name
   * License URL
   * Photo/video server identifier
   * Photo/video farm identifier
   * Photo/video secret
   * Photo/video secret original
   * Extension of the original photo
   * Photos/video marker (0 = photo, 1 = video)

The fields that contain free-form text have been URL-encoded. Not all fields may have a value, in particular the camera, title, description, tags, EXIF, longitude, latitude and accuracy fields may be empty. Note that the original extension is only meaningful for photos, not for videos (please inspect the first few bytes of the video to determine its file format).

In case researchers need photo/video content for their work, we kindly ask that they download the data responsibly, e.g. do not use a distributed system to download the photos and videos massively in parallel.

Note that, before publishing any metadata, photo or video in a report or elsewhere, it must be ensured that it is still publicly available (this includes data released as part of an expansion pack, see below). To do so, please check the photo/video page URL to see whether the data you want to publish is still available.


+++ MD5 Hashes +++

In addition to the dataset files, we supply a file containing photo/video identifiers and their corresponding MD5 hashes (yfcc100m_hash.bz2). These hashes are to be used for expansion packs (e.g. features, annotations) that are externally hosted, as a layer of indirection to hide direct access to the photo/video information.

Thus, if you wish to release data that refers to photos/videos from our dataset, please refer to their hashes instead of their identifiers. Other people wishing to use your data can then convert the hash to the identifier and lookup the corresponding metadata of the photo/video in our dataset. For example, if you wanted to release your own face detection expansion back (no face = 0, face = 1), then rather than specifying:

- 28605   0
- 29060   1
- 29205   0
- 29209   0
- 29294   0
- 29604   1

you would use the mapping to convert the identifiers to hashes and specify this instead in your expansion pack:

+ b75c2d5c2ed427a78037a8e67ed79b3   0
+ 41dd8720fc6b7ffac962e3121dab33    1
+ 4f9734a918719eb876217fe376d5a5df  0
+ 46b9a03fbd7e303f6c5bfe791d2d91b3  0
+ c1c2745ed4e221f2ba3521f0c449623f  0
+ 3871a12811f4fad5d95b31deb4ac38    1

Note that our own expansion packs will use the photo/video identifiers.


+++ Expansion packs +++

We currently offer the following expansion pack:

* Autotags v1 *
We used a deep learning approach to find the presence of a variety of concepts, such as people, animals, objects, food, events, architecture, and scenery. We trained 1,570 visual concept classifiers and applied them to the photos and videos (first frame). Each entry in this expansion pack (yfcc100m_autotags-v1.bz2) refers to a photo/video and to a (comma-separated) set of autotags and their (colon-separated) confidence scores.


+++ Citations +++

Finally, if you decide to use the YFCC100M dataset, please cite the following paper: "The New Data and New Challenges in Multimedia Research" by Bart Thomee, David A. Shamma, Gerald Friedland, Benjamin Elizalde, Karl Ni, Douglas Poland, Damian Borth, and Li-Jia Li, arXiv:1503.01817.


+++ Contact +++

In case of questions, please contact us at yfcc100m@yahoo-inc.com.
