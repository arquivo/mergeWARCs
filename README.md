# mergeWARCs

Script to Merge WARC files.

### Setup

```
git clone https://github.com/arquivo/mergeWARCs.git
cd mergeWARCs
pip install --upgrade virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
### Run

```
python MergeWARC.py
```

### Parameters

<pre>
-p or --path        --> Localization of the patching files
-d or --destination --> Destination of the patching files merged
-n or --filename    --> Filename_template of the patching files merged
-e or --extension   --> Extension of originated files
-s or --size        --> Size of the files merged (MB)
</pre>

### Example

Example and default parameters:

```
python MergeWARC.py -p ./PATCHING2019/ -d ./MergePatching/ -n patching-merged-{timestamp}-{random}.warc.gz -e warc.gz -s 100
```

### Authors

- [Pedro Gomes](pedro.gomes.fccn@gmail.com)
