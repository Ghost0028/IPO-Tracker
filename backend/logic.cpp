// Planning to make a cpp code which can help me read csv and json 
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

string extract_gmp_percentage(const std::string& gmp_str) {
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
    string price=ipo["price"];
    string gmp =ipo["gmp"];//"\u20b9-- (0.00%) L\/H (\u20b9): 0 \u2193 \/ 0 \u2191" need to extract the () part from it
    gmp=extract_gmp_percentage(gmp);
    ipo["gmp"]=gmp;
    string lot_size =ipo["Lot_size"];

    string qib_subscription_rate =ipo["QIB"];
    qib_subscription_rate=update_subs_rate(qib_subscription_rate);
    ipo["QIB"]=qib_subscription_rate;
    
    string nii_subscription_rate =ipo["NII"];
    nii_subscription_rate=update_subs_rate(nii_subscription_rate);
    ipo["NII"]=nii_subscription_rate;

    string retail_subscription_rate =ipo["Retail"];
    retail_subscription_rate=update_subs_rate(retail_subscription_rate);
    ipo["Retail"]=retail_subscription_rate;

    int close_date=ipo["close_date"];
    ipo["Minimum Capital"]=stoi(lot_size)*stoi(price);
    


  }
  ofstream out("ipo_react.json");
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
 


