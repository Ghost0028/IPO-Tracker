// Planning to make a cpp code which can help me read json 
// information and process it.
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>
#include <regex>
#include <iomanip>
#include "json.hpp"

using json= nlohmann::json;
using namespace std;

string extract_gmp_percentage(const string& gmp_str) {
    regex pattern(R"(\((\d+(?:\.\d+)?\%)\))");
    smatch matches;
    if (regex_search(gmp_str, matches, pattern)) {
        
        return matches[1].str();
    }
  
    return "0.00%";
} 
string update_subs_rate(string sub_rate){
   
  stringstream ss;
  //Handle the case of no subscription seperately
  if(sub_rate[0]=='0') return "<1% ~100%"; 
  double chance = 1.0/stod(sub_rate) *100;
  ss<<sub_rate<<" "<<fixed<<setprecision(2)<<chance<<"%";
  

  return ss.str();

}
string cutBeforeKeyword(const string& name) { 
    string keywords[] = {"NSE", "BSE","IPO"};
     for (const auto& kw : keywords) {
     size_t pos = name.find(kw); 
        if (pos != string::npos) { 
            return name.substr(0, pos ); 
    } } 
    return name; // no keyword found, return original 
}
void readJson(const string &inputPath,const string &outputPath){
    ifstream file (inputPath);
if (!file.is_open()){  // In case there is no such file present prints error
    
    cerr<<"Could not open file"<<endl;
    return ;
  }
  json j;
  file>>j;
  for(  auto &ipo : j){
    string name= ipo.value("Name","");
    ipo["Name"]=cutBeforeKeyword(name);
    double price= ipo.value("Price",0);
    string gmp =ipo.value("GMP","₹-- (0.00%)");//"\u20b9-- (0.00%) L\/H (\u20b9): 0 \u2193 \/ 0 \u2191" need to extract the () part from it
    gmp=extract_gmp_percentage(gmp);
    ipo["GMP"]=gmp;
    double lot_size =ipo.value("Lot_size",0);
    double temp=0.0;
    temp=ipo.value("QIB",0.0);
    string qib_subscription_rate =to_string(temp);
    qib_subscription_rate=update_subs_rate(qib_subscription_rate);
    ipo["QIB"]=qib_subscription_rate;
    
    temp=ipo.value("NII",0.0);
    string nii_subscription_rate =to_string(temp);
    nii_subscription_rate=update_subs_rate(nii_subscription_rate);
    ipo["NII"]=nii_subscription_rate;

    temp=ipo.value("Retail",0.0);
    string retail_subscription_rate =to_string(temp);
    retail_subscription_rate=update_subs_rate(retail_subscription_rate);
    ipo["Retail"]=retail_subscription_rate;
    if(lot_size==0) ipo["Minimum_Capital"]= "Lot size to be declared";
    else{
    if(ipo["Type"]=="SME")
    ipo["Minimum_Capital"]=lot_size*price*2;
    else
    ipo["Minimum_Capital"]=lot_size*price;  
    }
  }
  ofstream out(outputPath);
    if (out.is_open()) {
        out << j.dump(4);  // indent=4 for readability
        cout << "💾 Saved: ipo_react.json (React-ready)" << endl;
        out.close();
    } else {
        cerr << "❌ Failed to write ipo_react.json" << endl;
    }
}


int main(int argc ,char * argv[]){
    if (argc < 3) { cerr << "Usage: logic <input_json> <output_json>" << endl; return 1; } 
    string inputPath = argv[1]; 
    string outputPath = argv[2];
    readJson(inputPath,outputPath);
    return 0;
  };
 


