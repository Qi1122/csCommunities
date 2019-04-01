echo "---------- Making necessary directories ----------"
cd python
mkdir data
mkdir graphs
cd graphs
mkdir graph_data
cd ..
cd data
echo "---------- Downloading data ----------"
wget https://lfs.aminer.cn/lab-datasets/citation/dblp.v10.zip || curl -O https://lfs.aminer.cn/lab-datasets/citation/dblp.v10.zip
unzip *.zip
cd dblp-ref
mv *.json ..
cd ..
rm -rf *.zip
rm -rf dblp-ref
cd ../..
echo "---------- Create .gitignore ----------"
touch .gitignore
echo 'python/data/' > .gitignore
echo 'python/graphs/' >> .gitignore
echo "---------- Writing data (can take a while) ----------"
cd python
Rscript scrape_communities.R
python fuzzy_community_match.py
python process_data.py
python build_graph.py
