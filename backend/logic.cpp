#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>
#include <regex>
#include <iomanip>
#include "json.hpp"

using json = nlohmann::json;
using namespace std;

string extract_gmp_percentage(const string& gmp_str) {
    regex pattern(R"(\((\d+(?:\.\d+)?\%)\))");
    smatch matches;
    if (regex_search(gmp_str, matches, pattern)) {
        return matches[1].str();
    }
    return "0.00%";
}

string update_subs_rate(const string& sub_rate) {
    stringstream ss;
    if (sub_rate.empty() || sub_rate[0] == '0') return "<1% ~100%";
    try {
        double chance = 1.0 / stod(sub_rate) * 100;
        ss << sub_rate << " " << fixed << setprecision(2) << chance << "%";
        return ss.str();
    } catch (...) {
        cerr << "⚠️ Invalid subscription rate: " << sub_rate << endl;
        return sub_rate;
    }
}

int readJson(const string& inputPath, const string& outputPath) {   // 🔹 CHANGED: accept paths as arguments
    ifstream file(inputPath);
    if (!file.is_open()) {
        cerr << "❌ Could not open input file: " << inputPath << endl;
        return 1; // non-zero exit signals failure
    }

    json j;
    try {
        file >> j;
    } catch (const std::exception& e) {
        cerr << "❌ Failed to parse JSON: " << e.what() << endl;
        return 1;
    }

    for (auto& ipo : j) {
        string price = ipo.value("Price", "0");
        string lot_size = ipo.value("Lot_size", "0");

        string gmp = ipo.value("GMP", "₹-- (0.00%)");
        ipo["GMP"] = extract_gmp_percentage(gmp);

        ipo["QIB"] = update_subs_rate(ipo.value("QIB", "0.0%"));
        ipo["NII"] = update_subs_rate(ipo.value("NII", "0.0%"));
        ipo["Retail"] = update_subs_rate(ipo.value("Retail", "0.0%"));

        try {
            int lot = stoi(lot_size);
            int prc = stoi(price);
            if (ipo.value("Type", "") == "SME")
                ipo["Minimum_Capital"] = lot * prc * 2;
            else
                ipo["Minimum_Capital"] = lot * prc;
        } catch (...) {
            cerr << "⚠️ Invalid numeric values for lot_size or price" << endl;
            ipo["Minimum_Capital"] = 0;
        }
    }

    ofstream out(outputPath);   // 🔹 CHANGED: use outputPath directly, no "../"
    if (out.is_open()) {
        out << j.dump(4);
        cout << "💾 Saved: " << outputPath << endl;
        out.close();
        return 0;
    } else {
        cerr << "❌ Failed to write output file: " << outputPath << endl;
        return 1;
    }
}

int main(int argc, char* argv[]) {
    // 🔹 CHANGED: allow passing input/output paths via CLI args
    string inputPath = "./ipo_dashboard.json";
    string outputPath = "./ipo_react.json";  // default relative path

    if (argc > 2) {
        inputPath = argv[1];
        outputPath = argv[2];
    }

    return readJson(inputPath, outputPath); // 🔹 CHANGED: pass paths into function
}
