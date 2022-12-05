using System;
using System.Collections.Generic;
using System.IO;

namespace advent_of_code_2022
{
    public class day_01
    {
        public static int Main(string[] args)
        {
            string inputPath = "input.txt";
            List<int> calories = new();
            if (args.Length > 0)
            {
                inputPath = args[0];
            }
            // Console.WriteLine($"Input Path: \"{inputPath}\"");
            int total = 0;
            foreach(string line in File.ReadLines(inputPath))
            {
                if (line.Trim().Length > 0)
                {
                    // Read a number
                    if (Int32.TryParse(line, out int current))
                    {
                        total += current;
                    }
                    else
                    {
                        Console.WriteLine($"Error: Could not parse \"{line}\".");
                        return -1;
                    }
                }
                else
                {
                    if (total != 0)
                    {
                        calories.Add(total);
                        total = 0;
                    }
                }
            }

            /*
            int counter = 0;
            foreach(int calorie in calories)
            {
                counter++;
                Console.WriteLine($"{counter}\t{calorie}");
            }
            */
            // Part 1
            Console.WriteLine(Part1(calories));

            // Part 2
            Console.WriteLine(Part2(calories));
            return 0;
        }

        static int Part1(List<int> elfCalories)
        {
            return elfCalories.Max();
        }

        static int Part2(List<int> elfCalories)
        {
            return (
                from calories in elfCalories
                orderby calories descending
                select calories).Take(3).Sum();
        }
    }
}