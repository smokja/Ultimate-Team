using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

namespace sub_process
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> text = new List<string>();
            foreach (var line in File.ReadAllLines("players.json")) {
                // Convert json object to csv line
                var result = JsonConvert.DeserializeObject<Dictionary<string, Dictionary<string, string>>>(line);
                foreach (var key in result) {
                    string currentText = key.Key;
                    
                    foreach (var secondKey in key.Value) {
                        currentText += ","+secondKey.Value;
                    }

                    text.Add(currentText);
                }
            }
          

            File.WriteAllLines("players.csv", text);
        }
    }
}
