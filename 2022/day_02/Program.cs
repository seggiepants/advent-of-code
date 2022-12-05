using System;
using System.Collections.Generic;
using System.IO;

namespace advent_of_code_2022
{
    public class day_02
    {
        public static int Main(string[] args)
        {
            // 17472 too high
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
            
            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Console.WriteLine(Part2(data));
            return 0;
        }

        static List<Tuple<String, String>> Load(string path)
        {
            List<Tuple<String, String>> data = new();

            foreach(string line in File.ReadLines(path))
            {
                string[] chars = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                if (chars.Length >= 2)
                {
                    string first = chars[0].Trim();
                    string second = chars[1].Trim();
                    if (((first == "A") || (first == "B") || (first == "C")) &&
                        ((second == "X") || (second == "Y") || (second == "Z")))
                    {
                        data.Add(new Tuple<String, String>(first, second));
                    }
                    else
                    {
                        Console.WriteLine($"Error, unalbe to parse line \"{line}\"");
                    }
                }
            }

            return data;
        }

        static int Score(List<Tuple<String, String>> data)
        {
            int result = 0;
            Dictionary<String, int> lookup = new();
            // Shape: Rock = 1, Paper = 2, Scissors = 3
            // Outcome: Lose = 0, Draw = 3, Win = 6
            // Score = Shape + Outcome
            const int ROCK = 1, PAPER = 2, SCISSORS = 3;
            const int LOSE = 0, DRAW = 3, WIN = 6;
            lookup.Add("AX", ROCK + DRAW);
            lookup.Add("AY", PAPER + WIN);
            lookup.Add("AZ", SCISSORS + LOSE);

            lookup.Add("BX", ROCK + LOSE);
            lookup.Add("BY", PAPER + DRAW);
            lookup.Add("BZ", SCISSORS + WIN);
            
            lookup.Add("CX", ROCK + WIN);
            lookup.Add("CY", PAPER + LOSE);
            lookup.Add("CZ", SCISSORS + DRAW);

            int line = 0;
            foreach(Tuple<String, String>row in data)
            {
                line++;
                int score = lookup[row.Item1 + row.Item2];
                result += score;
                //Console.WriteLine($"line: {line}: - {row.Item1} vs. {row.Item2}, Score: {score} Total: {result}");
            }
            
            return result;
        }

        static void PrintData(List<Tuple<String, String>> data)
        {
            foreach(Tuple<String, String> row in data)
            {
                Console.WriteLine($"{row.Item1}, {row.Item2}");
            }
        }

        static int Part1(List<Tuple<String, String>> data)
        {
            return Score(data);
        }

        static int Part2(List<Tuple<String, String>> data)
        {
            const string ROCK = "X", PAPER = "Y", SCISSORS = "Z";
            Dictionary<string, string> lookup = new();
            lookup.Add("AX", SCISSORS); 
            lookup.Add("AY", ROCK); 
            lookup.Add("AZ", PAPER); 

            lookup.Add("BX", ROCK); // Paper Lose = Scissors
            lookup.Add("BY", PAPER); // Paper Draw = Paper
            lookup.Add("BZ", SCISSORS); // Paper Win = Rock
            
            lookup.Add("CX", PAPER); // Scissors Lose = Rock
            lookup.Add("CY", SCISSORS); // Scissors Draw = Scissors
            lookup.Add("CZ", ROCK); // Scissors Win = Paper
            List<Tuple<String, String>> reformattedData = new();
            foreach(Tuple<String, String> row in data)
            {
                // A, B, C = Rock, Paper, Scissors
                // X, Y, Z = Desired Outcomes of Lose, Win, Draw
                reformattedData.Add(new Tuple<string, string>(row.Item1, lookup[row.Item1 + row.Item2]));
            }
            //PrintData(reformattedData);
            return Score(reformattedData);
        }
    }
}