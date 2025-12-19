// Planning to make a cpp code which can help me read csv and json 
// information and process it.
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include "json.hpp"

using json= nlohmann::json;
using namespace std;

// initially it would be based on static data before scaling it.
// we can streamline the input and storing process further once we get the csv
//format example which would make things simpler
// make two diff functions for csv and json
//make a third function which does the actual calculation which will be called by the other two
void calculate(int issueprice, int gmp ,int subscriptionrate){
    double listingPrice= issueprice *(1+ (gmp*1.0/issueprice));
    double estimatedProbability= 1.0/subscriptionrate;

    cout<<"Expected Listing price = "<<listingPrice<<endl;
    cout<<"1 in "<<subscriptionrate<<" will get an allotment that is "<<setprecision(2)<<fixed<<estimatedProbability*100<<" % "<<endl;

} //can be further cateegorised into categories like hni etc
void readJson(){
    ifstream file ("data.json");
if (!file.is_open()){  // In case there is no such file present prints error
    
    cerr<<"Could not open file"<<endl;
    return ;
  }

  json j;
  file>>j;

  for( const auto &ipo : j){
    
    string name=ipo["ipo"];
    int price= ipo["issuePrice"];
    int gmp =ipo["gmp"];
    double subscriptionrate=ipo["subscription"];
    cout<<name<<" "<<price<<" "<<gmp<<""<<endl;
    calculate(price,gmp,subscriptionrate);


  }
}
void readCsv(){
  ifstream file ("data.csv");
  
  if (!file.is_open()){  // In case there is no such file present prints error
    cerr<<"Could not open file"<<endl;
    return ;
  }
  string line;
  getline(file,line); // this line will be needed incase the data has a useless header
  stringstream ss(line);
    string cell;
    vector <string> heading;
    while(getline(ss,cell,',')){
        heading.push_back(cell);
    }

  while(getline(file,line)){
    stringstream strs(line);
    string data;
    vector <string> rows;
    while(getline(strs,data,',')){
        rows.push_back(data);
    }
    int c=0;
    for (const auto& k : rows){
     //checking working
         cout <<heading[c]<<" "<< k << " ";
         
         c++;
    } 
    calculate(stoi(rows[1]),stoi(rows[2]),stoi(rows[3]));
    cout << "\n---------------\n";
}
}
int main(){
    readJson();
  };
 


