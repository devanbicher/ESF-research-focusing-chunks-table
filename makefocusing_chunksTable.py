import os,tempfile



def parsefocusingfile(filename):
    focfile = open(filename,'r');
    chunklist = [];
    for l in focfile.readlines():
        if l.startswith("Volume of Fragment"):
            splitline = l.strip().split();
            vol = splitline[-1];
            chunkname = splitline[-2].split('/')[-1].strip(']:');
            chunkfile = chunkname+".SURF";
            chunknum = chunkname.split('-')[-1];
            if os.path.exists("./chunky/"+chunkfile):
                chunklist.append([chunkfile,chunknum,vol]);
            else:
                print chunkfile +" Is missing, not added to list. Volume: "+vol;
                continue;
    
    return chunklist
    
def getdistances():
    distfile = open('protein-chunk.csv','r');
    distdict = {};
    for l in distfile.readlines():
        linesplit = l.strip().split(',');
        distdict[linesplit[0]] = linesplit[1];

    distfile.close();

    return distdict;

def main():
    csvfile = open('focusing-chunks.csv','w');
    sqlfile = open('focusing_chunks.sql','w');
    
    dists = getdistances();
    
    prots = [p for p in os.listdir("../../../") if len(p) == 4];
    #prots = ['1A1T']; #DEBUG   
    
    focusing = {'0_65':'0.65','1_25':'1.25','2_50':'2.50'}
    
    os.chdir('../../../scripts');
    
    for p in prots:
        os.chdir('../'+p);
        print "Now in "+p;
        for f in focusing.keys():
            chunkdetails = 'chunky/focChunks-'+f+'.txt';
            if os.path.exists(chunkdetails):
                chunks = parsefocusingfile(chunkdetails);
                if len(chunks) == 0:
                    print chunkdetails+" Contained no volume information";
                else:
                    for c in chunks:
                        if c[0] in dists:
                            csvfile.write(c[0]+','+c[1]+','+p+','+dists[c[0]]+','+c[2]+','+focusing[f]+"\n");
                            columns = "(chunk_file,chunk_num,pdb,pr_id,protein_distance,chunk_volume,threshold)"
                            selectprid = "(SELECT pr_id FROM protein_rna WHERE pdb='"+p+"')";
                            values =  "('"+c[0]+"',"+c[1]+",'"+p+"',"+selectprid+","+dists[c[0]]+","+c[2]+","+focusing[f]+")";
                            sqlfile.write("INSERT INTO focusing_chunks "+columns+" VALUES "+values+";\n");
                        else:
                            print c+" NOT in the distances list!";
            else:
                print chunkdetails+" Does not exist!";

    csvfile.close();
    sqlfile.close();
                

if __name__ == "__main__":
    main();



#fc_id
#chunk_file
#chunk_num
#pdb
#pr_id
#protein_distance
#chunk_volume
#threshold
