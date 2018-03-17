# to start using your module
cd ai_tutor
git pull origin master
cd ..
rm -rf temp
mkdir temp
mv ./ai_tutor ./temp
rm -rf ai_tutor
mv ./temp/ai_tutor/ai_tutor ./
#rm -rf temp


