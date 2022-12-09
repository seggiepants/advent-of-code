using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{
    public class day_09
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
            List<Tuple<String, int>> data = Load(inputPath);
            PrintData(data);

            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Console.WriteLine(Part2(data));

            return 0;
        }

        static List<Tuple<String, int>> Load(String path)
        {
            Regex cmd = new Regex(@"(?'dir'[LRUD]) (?'count'\d+)", RegexOptions.Compiled);
            List<Tuple<String, int>> data = new();

            int lineNum = 0;
            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (cmd.IsMatch(line))
                {
                    MatchCollection matches = cmd.Matches(line);
                    foreach(Match match in matches)
                    {
                        GroupCollection groups = match.Groups;    
                        string dir = groups["dir"].Value.Trim();
                    
                        if (!Int32.TryParse(groups["count"].Value, out int count))
                        {
                            Console.WriteLine($"Error Parsing file size for line #{lineNum}: {line}.");
                            break;
                        }
                        data.Add(new Tuple<String, int>(dir, count));
                    }
                }
            }
            return data;
        }

        static void PrintData(List<Tuple<String, int>> data)
        {
            foreach(Tuple<String, int> row in data)
            {
                Console.WriteLine($"{row.Item1}: {row.Item2}");
            }
        }

       
        static int Part1(List<Tuple<String, int>> data)
        {
            HashSet<Tuple<int, int>> tailPositions = new();
            int headX = 0, headY = 0, tailX = 0, tailY = 0;
            tailPositions.Add(new Tuple<int, int>(tailX, tailY));

            foreach(Tuple<String, int>cmd in data)
            {
                int dx = 0, dy = 0;
                switch(cmd.Item1)
                {
                    case "L":
                        dx = -1;
                        dy = 0;
                        break;
                    case "R":
                        dx = 1;
                        dy = 0;
                        break;
                    case "U":
                        dx = 0;
                        dy = -1;
                        break;
                    case "D":
                        dx = 0;
                        dy = 1;
                        break;
                    default:
                        Console.WriteLine($"Error invalid direction: {cmd.Item1}.");
                        break;
                }

                for(int i = 0; i < cmd.Item2; i++)
                {
                    headX += dx;
                    headY += dy;
                    
                    // Check if tail more than one space from head
                    int stepX = (headX - tailX);
                    int stepY = (headY - tailY);
                    if (Math.Abs(stepX) > 1 || Math.Abs(stepY) > 1)
                    {
                        tailX += Math.Sign(stepX);
                        tailY += Math.Sign(stepY);
                        tailPositions.Add(new Tuple<int, int>(tailX, tailY));
                    }
                }
            }

            return tailPositions.Count;
        }        

        static int Part2(List<Tuple<String, int>> data)
        {
            const int numNodes = 10;
            List<int>[] nodes = new List<int>[numNodes];
            for(int i = 0; i < numNodes; i++)
            {
                nodes[i] = new();
                nodes[i].Add(0); // x
                nodes[i].Add(0); // y
            }

            HashSet<Tuple<int, int>> tailPositions = new();            
            tailPositions.Add(new Tuple<int, int>(nodes[numNodes - 1][0], nodes[numNodes - 1][1]));

            foreach(Tuple<String, int>cmd in data)
            {
                int dx = 0, dy = 0;
                switch(cmd.Item1)
                {
                    case "L":
                        dx = -1;
                        dy = 0;
                        break;
                    case "R":
                        dx = 1;
                        dy = 0;
                        break;
                    case "U":
                        dx = 0;
                        dy = -1;
                        break;
                    case "D":
                        dx = 0;
                        dy = 1;
                        break;
                    default:
                        Console.WriteLine($"Error invalid direction: {cmd.Item1}.");
                        break;
                }

                for(int i = 0; i < cmd.Item2; ++i)
                {
                    nodes[0][0] += dx;
                    nodes[0][1] += dy;

                    for (int j = 1; j < nodes.Length; ++j)
                    {
                        // Check if tail more than one space from head
                        int stepX = (nodes[j - 1][0] - nodes[j][0]);
                        int stepY = (nodes[j - 1][1] - nodes[j][1]);
                        if (Math.Abs(stepX) > 1 || Math.Abs(stepY) > 1)
                        {
                            nodes[j][0] += Math.Sign(stepX);
                            nodes[j][1] += Math.Sign(stepY);
                        }
                    }
                    tailPositions.Add(new Tuple<int, int>(nodes[numNodes - 1][0], nodes[numNodes - 1][1]));
                }
            }

            return tailPositions.Count;
        }
    }
}