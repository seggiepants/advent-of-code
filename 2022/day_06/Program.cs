using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace advent_of_code_2022
{
    public class day_06
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
            string data = Load(inputPath);
            // PrintData(data);

            // Part 1
            Console.WriteLine(Part1(data));
            /*
            if (Part1("bvwbjplbgvbhsrlpgdmjqwftvncz") != 5)
                Console.WriteLine("Error on secondary test 1-1.");

            if (Part1("nppdvjthqldpwncqszvftbrmjlhg") != 6)
                Console.WriteLine("Error on secondary test 1-2.");

            if (Part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") != 10)
                Console.WriteLine("Error on secondary test 1-3.");

            if (Part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") != 11)
                Console.WriteLine("Error on secondary test 1-4.");
            */

            // Part 2
            Console.WriteLine(Part2(data));
            /* Extra Tests
            if (Part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") != 19)
                Console.WriteLine("Error on secondary test 2-1.");

            if (Part2("bvwbjplbgvbhsrlpgdmjqwftvncz") != 23)
                Console.WriteLine("Error on secondary test 2-2.");

            if (Part2("nppdvjthqldpwncqszvftbrmjlhg") != 23)
                Console.WriteLine("Error on secondary test 2-3.");

            if (Part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") != 29)
                Console.WriteLine("Error on secondary test 2-4.");

            if (Part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") != 26)
                Console.WriteLine("Error on secondary test 2-5.");
            */
            return 0;
        }

        static String Load(String path)
        {
            return File.ReadAllText(path).Trim();
        }

        static void PrintData(String data)
        {
            Console.WriteLine(data);
        }

        static int FindMessageStart(String data, int windowSize)
        {
            for(int i = 0; i < data.Length - windowSize; ++i)
            {
                char[] window = data.Substring(i, windowSize).ToCharArray();
                char[] distinctWindow = window.Distinct().ToArray();
                if (window.Length == distinctWindow.Length)
                {
                    return i + window.Length;
                }
            }
            return -1;
        }
        
        static int Part1(String data)
        {
            return FindMessageStart(data, 4);
        }        

        static int Part2(String data)
        {
            return FindMessageStart(data, 14);
        }
    }
}