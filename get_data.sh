cd python
mkdir data
mkdir graphs
cd data
wget https://lfs.aminer.cn/lab-datasets/citation/dblp.v10.zip || curl -O https://lfs.aminer.cn/lab-datasets/citation/dblp.v10.zip
unzip *.zip
rm -rf *.zip
cd ../..
touch .gitignore
echo 'python/data/' > .gitignore
echo 'python/graphs/' >> /gitignore
cd python
Rscript scraped_communities.R
python fuzzy_community_match.py
python build_community_graph.py
