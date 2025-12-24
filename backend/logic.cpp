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
void readJson(){
    ifstream file ("ipo_dashboard.json");
if (!file.is_open()){  // In case there is no such file present prints error
    
    cerr<<"Could not open file"<<endl;
    return ;
  }

  json j;
  file>>j;
  
  for(  auto &ipo : j){
    string price= ipo.value("Price","0");
    string gmp =ipo.value("GMP","₹-- (0.00%)");//"\u20b9-- (0.00%) L\/H (\u20b9): 0 \u2193 \/ 0 \u2191" need to extract the () part from it
    gmp=extract_gmp_percentage(gmp);
    ipo["GMP"]=gmp;
    string lot_size =ipo.value("Lot_size","0");

    string qib_subscription_rate =ipo.value("QIB","0.0%");
    qib_subscription_rate=update_subs_rate(qib_subscription_rate);
    ipo["QIB"]=qib_subscription_rate;
    
    string nii_subscription_rate =ipo.value("NII","0.0%");
    nii_subscription_rate=update_subs_rate(nii_subscription_rate);
    ipo["NII"]=nii_subscription_rate;

    string retail_subscription_rate =ipo.value("Retail","0.0%");
    retail_subscription_rate=update_subs_rate(retail_subscription_rate);
    ipo["Retail"]=retail_subscription_rate;
    if(ipo["Type"]=="SME")
    ipo["Minimum_Capital"]=stoi(lot_size)*stoi(price)*2;
    else
    ipo["Minimum_Capital"]=stoi(lot_size)*stoi(price);  
    


  }
  string react_path = "../ipo_tracker/public/ipo_react.json"; //so that it writes directly into the required place
  ofstream out(react_path);
    if (out.is_open()) {
        out << j.dump(4);  // indent=4 for readability
        cout << "💾 Saved: ipo_react.json (React-ready)" << endl;
        out.close();
    } else {
        cerr << "❌ Failed to write ipo_react.json" << endl;
    }
}


int main(){
    readJson();
    return 0;
  };
 


