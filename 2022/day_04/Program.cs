using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{
    public class day_04
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
            List<Tuple<int, int, int, int>> data = Load(inputPath);            
            // PrintData(data);

            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Console.WriteLine(Part2(data));
            
            return 0;
        }

        static bool FullyContains(int a1, int a2, int b1, int b2)
        {
            return ((a1 <= b1) && (a2 >= b2)) || ((b1 <= a1) && (b2 >= a2));
        }

        static bool Overlaps(int a1, int a2, int b1, int b2)
        {
            if (FullyContains(a1, a2, b1, b2))
            {
                return true;
            }

            return (FullyContains(a1, a2, b1, b2) ||
                (a1 <= b1 && a2 >= b1) ||
                (a1 <= b2 && a2 >= b2) ||
                (b1 <= a1 && b2 >= a1) ||
                (b1 <= a2 && b2 >= a2));
        }

        static List<Tuple<int, int, int, int>> Load(string path)
        {
            Regex r = new Regex(@"(?'a1'\d+)-(?'a2'\d+),(?'b1'\d+)-(?'b2'\d+)", RegexOptions.Compiled);

            List<Tuple<int, int, int, int>> data = new();

            foreach(string line in File.ReadLines(path))
            {
                line.Trim();
                MatchCollection matches = r.Matches(line);
                foreach(Match match in matches)
                {
                    GroupCollection groups = match.Groups;

                    if (!Int32.TryParse(groups["a1"].Value, out int a1))
                    {
                        String item = groups["a1"].Value;
                        Console.WriteLine($"Error Parsing line {line}, item {item}.");
                        return data;
                    }
                    if (!Int32.TryParse(groups["a2"].Value, out int a2))
                    {
                        String item = groups["a2"].Value;
                        Console.WriteLine($"Error Parsing line {line}, item {item}.");
                        return data;
                    }
                    if (!Int32.TryParse(groups["b1"].Value, out int b1))
                    {
                        String item = groups["b1"].Value;
                        Console.WriteLine($"Error Parsing line {line}, item {item}.");
                        return data;
                    }
                    if (!Int32.TryParse(groups["b2"].Value, out int b2))
                    {
                        String item = groups["b2"].Value;
                        Console.WriteLine($"Error Parsing line {line}, item {item}.");
                        return data;
                    }

                    data.Add(new Tuple<int, int, int, int>(a1, a2, b1, b2));
                }
            }
            return data;
        }

        static void PrintData(List<Tuple<int, int, int, int>> data)
        {
            int line = 0;
            foreach(Tuple<int, int, int, int> row in data)
            {
                line++;
                Console.WriteLine($"{line}: {row.Item1}, {row.Item2}, {row.Item3}, {row.Item4}");
            }
        }

        static int Part1(List<Tuple<int, int, int, int>> data)
        {
            int total = 0;
            foreach(Tuple<int, int, int, int>row in data)
            {
                if (FullyContains(row.Item1, row.Item2, row.Item3, row.Item4))
                {
                    total++;
                }
            }
            return total;
        }        
        static int Part2(List<Tuple<int, int, int, int>> data)
        {
            int total = 0;
            foreach(Tuple<int, int, int, int>row in data)
            {
                if (Overlaps(row.Item1, row.Item2, row.Item3, row.Item4))
                {
                    total++;
                }
            }
            return total;
        }
    }
}