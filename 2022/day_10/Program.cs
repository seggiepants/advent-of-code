using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{
    ////////////////////////////////////////////
    // Uh Oh, are we making a virtual machine!    
    ////////////////////////////////////////////

    public class ProcessorState
    {
        public int X {get; set;}
        public int PC {get; set;}
        public int CLK {get; set;}

        public ProcessorState()
        {
            Reset();
        }

        public void Reset()
        {
            X = 1;
            PC = 0;
            CLK = 0;
        }

        public void Tick()
        {
            ++CLK;
        }
    }

    public class day_10
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

            List<Tuple<String, int>> data = Load(inputPath);
            // PrintData(data);

            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Part2(data);

            return 0;
        }

        static List<Tuple<String, int>> Load(String path)
        {
            Regex addx = new Regex(@"(?'cmd'addx) (?'amt'(\-|\+)?(\d+))", RegexOptions.Compiled);
            Regex noop = new Regex(@"(?'cmd'noop)", RegexOptions.Compiled);
            List<Tuple<String, int>> data = new();

            int lineNum = 0;
            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (addx.IsMatch(line))
                {
                    MatchCollection matches = addx.Matches(line);
                    foreach(Match match in matches)
                    {
                        GroupCollection groups = match.Groups;    
                        string cmd = groups["cmd"].Value.Trim();
                    
                        if (!Int32.TryParse(groups["amt"].Value, out int amt))
                        {
                            Console.WriteLine($"Error Parsing file size for line #{lineNum}: {line}.");
                            break;
                        }
                        data.Add(new Tuple<String, int>(cmd, amt));
                    }
                }
                else if(noop.IsMatch(line))
                {
                    // We already know all we need, don't bother parsing further.
                    data.Add(new Tuple<String, int>("noop", 0));
                }
            }
            return data;
        }

        static void PrintData(List<Tuple<String, int>> data)
        {
            foreach(Tuple<String, int> row in data)
            {
                if (row.Item1 == "noop")
                {
                    Console.WriteLine("noop");
                }
                else
                {
                    Console.WriteLine($"{row.Item1}: {row.Item2}");
                }
            }
        }

        // I found an excuse to use Yield.
        static IEnumerable<int> Simulate(List<Tuple<String, int>> program, ProcessorState state)
        {
            int lineNumber = 0;
            foreach(Tuple<String, int>cmd in program)
            {
                ++lineNumber;
                if (cmd.Item1 == "noop")
                {
                    state.Tick();
                    yield return state.CLK;
                }
                else if (cmd.Item1 == "addx")
                {
                    state.Tick();
                    yield return state.CLK;
                    state.Tick();
                    yield return state.CLK;
                    state.X += cmd.Item2;
                }
                else 
                {
                    Console.WriteLine($"Error: Unrecognized command: \"{cmd.Item1}\" on line {lineNumber}.");
                    break;
                }
            }
        }

        static int Part1(List<Tuple<String, int>> program)
        {
            List<int> samplePoints = new() {20, 60, 100, 140, 180, 220};
            ProcessorState state = new();
            int sumSignalStrength = 0;
            foreach(int tick in Simulate(program, state))
            {
                if (samplePoints.Contains(tick))
                {
                    int signalStrength = tick * state.X;
                    sumSignalStrength += signalStrength;
                    // Console.WriteLine($"tick: {tick}, signalStrength: {signalStrength}, sum: {sumSignalStrength}.");
                }
            }
            return sumSignalStrength;
        }        

        static void Part2(List<Tuple<String, int>> program)
        {            
            ProcessorState state = new();
            string row = "";
            foreach(int tick in Simulate(program, state))
            {
                int index = row.Length + 1;
                if ((index == state.X) || (index == state.X + 1) || (index == state.X + 2))
                {
                    row += "#";
                }
                else
                {
                    row += ".";
                }

                if (row.Length == 40)
                {
                    Console.WriteLine(row);
                    row = "";
                }
            }
            // Last partial row?
            if (row.Length > 0)
                Console.WriteLine(row);
        }
    }
}