using System;
using System.Collections.Generic;
using System.IO;

namespace advent_of_code_2022
{
    public class day_03
    {
        public static int Main(string[] args)
        {
            string inputPath = "input.txt";
            if (args.Length > 0)
            {
                inputPath = args[0];
            }

            if (!File.Exists(inputPath))
            {
                Console.WriteLine($"Error: File Not Found \"{inputPath}\"");
                return -1;
            }

            // Console.WriteLine($"Input Path: \"{inputPath}\"");
            List<Tuple<String, String>> data = Load(inputPath);            
            // PrintData(data);

            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Console.WriteLine(Part2(data));

            return 0;
        }

        static char FindCommon(string first, string second)
        {
            foreach(char c in first)
            {
                if (second.Contains(c))
                {
                    return c;
                }
            }
            return ' ';
        }

        static char FindCommon(string first, string second, string third)
        {
            foreach(char c in first)
            {
                if (second.Contains(c) && third.Contains(c))
                {
                    return c;
                }
            }
            return ' ';
        }

        static List<Tuple<String, String>> Load(string path)
        {
            List<Tuple<String, String>> data = new();

            foreach(string line in File.ReadLines(path))
            {
                line.Trim();
                int middle = (line.Length / 2);
                data.Add(new Tuple<string, string>(line.Substring(0,middle), line.Substring(middle)));
            }

            return data;
        }

        static int Score(char common)
        {
            const string lower = "abcdefghijklmnopqrstuvwxyz";
            const string upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

            int index = lower.IndexOf(common);
            if (index >= 0)
            {
                return index + 1;
            }
            index = upper.IndexOf(common);
            if (index >= 0)
            {
                return index + 27;
            }
            return 0;
        }

        static void PrintData(List<Tuple<String, String>> data)
        {
            foreach(Tuple<String, String> row in data)
            {
                Console.WriteLine($"{row.Item1}, {row.Item2} | Common = {FindCommon(row.Item1, row.Item2)} | Score = {Score(FindCommon(row.Item1, row.Item2))}");
            }
        }

        static int Part1(List<Tuple<String, String>> data)
        {
            int total = 0;
            foreach(Tuple<String, String>row in data)
            {
                total += Score(FindCommon(row.Item1, row.Item2));
            }
            return total;
        }

        static int Part2(List<Tuple<String, String>> data)
        {
            int total = 0;
            for(int i = 0; i < data.Count; i+=3)
            {
                string first = data[i].Item1 + data[i].Item2;
                string second = data[i + 1].Item1 + data[i + 1].Item2;
                string third = data[i + 2].Item1 + data[i + 2].Item2;
                char common = FindCommon(first, second, third);
                total += Score(common);
            }
            return total;
        }
    }
}