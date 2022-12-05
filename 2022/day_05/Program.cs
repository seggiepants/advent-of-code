using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{
    public class day_05
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
            Dictionary<int, List<String>> dock = new();
            List<Tuple<int, int, int>> moves = new();
            Load(inputPath, dock, moves);
            //PrintData(dock, moves);

            // Part 1
            Console.WriteLine(Part1(CopyDock(dock), moves));

            // Part 2
            Console.WriteLine(Part2(CopyDock(dock), moves));
            
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

        static void Load(string path, Dictionary<int, List<String>> dock, List<Tuple<int, int, int>> moves)
        {
            Regex r = new Regex(@"move (?'count'\d+) from (?'source'\d+) to (?'destination'\d+)", RegexOptions.Compiled);

            // Search for the bottom of the dock
            int dockRow = 0;
            bool foundDock = false;
            string[] lines = File.ReadAllLines(path);
            for(int i = 0; i < lines.Count(); i++)
            {
                if (lines[i].Substring(0, 3).Equals(" 1 "))
                {
                    foundDock = true;
                    dockRow = i;
                    break;
                }
            }
            if (!foundDock)
            {
                Console.WriteLine("Unable to find the dock.");
                return;
            }

            // Get the dock numbers.
            string dockLine = lines[dockRow];
            List<int> dockIndexes = new List<int>();
            for(int i = 0; i < dockLine.Length; i+= 4)
            {
                string dockNum = dockLine.Substring(i, 3);
                if (!Int32.TryParse(dockNum, out int index))
                {
                    Console.WriteLine($"Bad Dock Name: {dockNum}.");
                    return;
                }
                else
                {
                    dockIndexes.Add(index);
                    dock.Add(index, new List<String>());
                }
            }
            for (int i = dockRow - 1; i >= 0; i--)
            {
                string row = lines[i];
                int index = -1;
                for(int j = 0; j < row.Length; j+= 4)
                {
                    index++;
                    string container = row.Substring(j, 3).Trim();
                    if (container.Length > 0)
                    {
                        dock[dockIndexes[index]].Add(container);
                    }
                }
            }

            for(int i = dockRow + 1; i < lines.Length; i++)
            {
                MatchCollection matches = r.Matches(lines[i]);
                foreach(Match match in matches)
                {
                    GroupCollection groups = match.Groups;
                    if (!Int32.TryParse(groups["count"].Value, out int count))
                    {
                        String item = groups["count"].Value;
                        Console.WriteLine($"Error Parsing line {lines[i]}, item {item}.");
                        return;
                    }
                    if (!Int32.TryParse(groups["source"].Value, out int source))
                    {
                        String item = groups["source"].Value;
                        Console.WriteLine($"Error Parsing line {lines[i]}, item {item}.");
                        return;
                    }
                    if (!Int32.TryParse(groups["destination"].Value, out int destination))
                    {
                        String item = groups["destination"].Value;
                        Console.WriteLine($"Error Parsing line {lines[i]}, item {item}.");
                        return;
                    }
                    moves.Add(new Tuple<int, int, int>(count, source, destination));
                }
            }
            /*
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
            */
        }

        static void PrintData(Dictionary<int, List<String>> dock, List<Tuple<int, int, int>> moves)
        {

            foreach(KeyValuePair<int, List<String>> row in dock)
            {
                Console.WriteLine($"{row.Key}: {String.Join(",", row.Value)}");
            }

            foreach(Tuple<int, int, int> row in moves)
            {
                Console.WriteLine($"Move {row.Item1} containers from dock {row.Item2} to dock {row.Item3}.");
            }
        }

        static Dictionary<int, List<String>> CopyDock(Dictionary<int, List<string>> source)
        {
            Dictionary<int, List<String>> dock = new();
            foreach(int key in source.Keys)
            {
                dock.Add(key, new List<String>());
                foreach(string value in source[key])
                {
                    dock[key].Add(value);
                }
            }
            return dock;
        }

        static String Part1(Dictionary<int, List<String>> dock, List<Tuple<int, int, int>> moves)
        {
            foreach(Tuple<int, int, int>row in moves)
            {
                int count = row.Item1;
                int source = row.Item2;
                int dest = row.Item3;
                List<string> from = dock[source];
                List<string> to = dock[dest];
                for(int i = 0; i < count; i++)
                {
                    // Pop
                    string value = from[from.Count - 1];
                    from.RemoveAt(from.Count - 1);

                    // Push
                    to.Add(value);
                }
            }

            string ret = "";
            foreach(int key in dock.Keys)
            {
                ret += dock[key][dock[key].Count - 1];
            }
            ret = ret.Replace("[", "", false, null);
            ret = ret.Replace("]", "", false, null);
            return ret;
        }        
        static String Part2(Dictionary<int, List<String>> dock, List<Tuple<int, int, int>> moves)
        {
            foreach(Tuple<int, int, int>row in moves)
            {
                int count = row.Item1;
                int source = row.Item2;
                int dest = row.Item3;
                List<string> from = dock[source];
                List<string> to = dock[dest];
                int removeAt = from.Count - count;
                //Console.WriteLine($"{String.Join(",", from)}, removeAt: {removeAt}, count: {count}");
                for(int i = removeAt; i < from.Count; i++)
                {
                    // Peek
                    string value = from[i];

                    // Push
                    to.Add(value);
                }
                // Pop
                from.RemoveRange(removeAt, count);
            }

            string ret = "";
            foreach(int key in dock.Keys)
            {
                ret += dock[key][dock[key].Count - 1];
            }
            ret = ret.Replace("[", "", false, null);
            ret = ret.Replace("]", "", false, null);
            return ret;
        }
    }
}