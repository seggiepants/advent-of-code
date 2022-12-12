using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{
    public class Map
    {
        public List<List<char>> grid {get; set;}
        public int startX { get; set;}
        public int startY { get; set;}
        public int targetX { get; set;}
        public int targetY { get; set;}

        public Map()
        {
            Reset();
        }

        public void Reset()
        {
            startX = 0;
            startY = 0;
            targetX = 0;
            targetY = 0;
            grid = new();
        }
    }

    public class day_12
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

            Map data = Load(inputPath);            
            // PrintData(data, new List<Tuple<int, int>>());

            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Console.WriteLine(Part2(data));

            return 0;
        }

        static Map Load(String path)
        {
            Map data = new();

            int lineNum = 0;
            int rowNum = 0;
            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (line.Length > 0)
                {   
                    List<char> current = new  List<char>();
                    int colNum = 0;                
                    foreach(char c in line)
                    {
                        if (c == 'S')
                        {
                            data.startX = colNum;
                            data.startY = rowNum;
                            current.Add('a');                            
                        }
                        else if (c == 'E')
                        {
                            data.targetX = colNum;
                            data.targetY = rowNum;
                            current.Add('z');                            
                        }
                        else if (c >= 'a' && c <= 'z')
                        {
                            current.Add(c);
                        }
                        colNum++;
                    }
                    data.grid.Add(current);
                    rowNum++;
                }
            }
            return data;
        }

        static void PrintData(Map data, List<Tuple<int, int>> path)
        {
            int y = 0;
            foreach(List<char> row in data.grid)
            {
                int x = 0;
                foreach(char c in row)
                {
                    if (path.Contains(new Tuple<int, int>(x, y)))
                    {
                        Console.Write('.');
                    }
                    else
                    {
                        Console.Write(c);
                    }
                    x++;
                }
                y++;
                Console.WriteLine("");
            }
            Console.WriteLine($"Start: ({data.startX},{data.startY})");
            Console.WriteLine($"Target: ({data.targetX},{data.targetY})");
        }

        static int Dijkstra(Map data)
        {
            Tuple<int, int> dest = new Tuple<int, int>(data.targetX, data.targetY);
            List<Tuple<int, int>> queue = new();
            Dictionary<Tuple<int, int>, int> dist = new();
            Dictionary<Tuple<int, int>, Tuple<int, int>> prev = new();

            for(int j = 0; j < data.grid.Count; ++j)
            {
                for(int i = 0; i < data.grid[j].Count; ++i)
                {
                    Tuple<int, int> pos = new(i, j);
                    dist[pos] = Int32.MaxValue; // Max int value is the infinity stand-in.
                    prev[pos] = new Tuple<int, int>(-1, -1); // -1, -1 is the null stand-in.
                    queue.Add(pos);
                }
            }

            List<Tuple<int, int>> neighborDelta = new();
            neighborDelta.Add(new Tuple<int, int>(0, -1)); // up
            neighborDelta.Add(new Tuple<int, int>(-1, 0)); // left
            neighborDelta.Add(new Tuple<int, int>(0, 1)); // down
            neighborDelta.Add(new Tuple<int, int>(1, 0)); // right.
            dist[new Tuple<int, int>(data.startX, data.startY)] = 0;

            while (queue.Count > 0)
            {
                Tuple<int, int> minPos = 
                    (from pair in dist
                    join item in queue on pair.Key equals item
                    orderby pair.Value ascending
                    select pair.Key).First();
                if (minPos.Equals(dest))
                  break;

                queue.Remove(minPos);
                foreach(Tuple<int, int>delta in neighborDelta)
                {
                    int x = minPos.Item1 + delta.Item1;
                    int y = minPos.Item2 + delta.Item2;
                    Tuple<int, int> neighbor = new(x, y);
                    // Check in bounds of the map.
                    if (dist.Keys.Contains(neighbor))
                    {                        
                        //if (queue.Contains(neighbor))
                        //{
                            // Can only go if delta value <= 1
                            int minValue = (int)data.grid[minPos.Item2][minPos.Item1];
                            int neighborValue = (int)data.grid[y][x];
                            int deltaValue = neighborValue - minValue;
                            if (deltaValue <= 1)
                            {
                                int newDist = dist[minPos] + 1;
                                int currentDist = dist[neighbor];
                                if (newDist < currentDist)
                                {
                                    dist[neighbor] = newDist;
                                    prev[neighbor] = minPos;
                                }
                            }
                        //}
                    }
                }
            }
            Tuple<int, int> source = new(data.startX, data.startY);
            Tuple<int, int> target = new(data.targetX, data.targetY);
            Tuple<int, int> nullValue = new(-1, -1);
            List<Tuple<int, int>> path = new();
            if((prev.Keys.Contains(target)) || (target.Equals(source)))
            {
                bool ok = true;
                while (ok)
                {
                    path.Insert(0, target);
                    if (target.Equals(source))
                        break;

                    ok = prev.Keys.Contains(target) && !prev[target].Equals(nullValue);                        
                    if (ok)
                    {
                        target = prev[target];
                        if (path.Contains(target))
                            ok = false;
                    }

                }
                /*
                foreach(Tuple<int, int> node in path)
                {
                    Console.Write($" ({node.Item1}, {node.Item2})");
                }
                Console.WriteLine("");
                */
                
                
            }
            /*
            foreach(Tuple<int, int> pos in path)
            {
                Console.Write($"[{pos.Item1}, {pos.Item2}] ");
            }
            Console.WriteLine("");
            */
            // 523 is too high for part 2
            if (target.Equals(source))
                return path.Count - 1; 
            else
                return int.MaxValue;
        }

        static int Part1(Map data)
        {
            return Dijkstra(data);
        }

        static int Part2(Map data)
        {   
            int minValue = int.MaxValue;
            for(int j = 0; j < data.grid.Count;++j)
            {
                for(int i = 0; i < data.grid[j].Count;++i)
                {
                    if (data.grid[j][i] == 'a')
                    {
                        data.startX = i;
                        data.startY = j;
                        int currentValue = Dijkstra(data);
                        if (currentValue < minValue)
                            minValue = currentValue;
                        Console.WriteLine($"({i},{j}) = {currentValue} vs. {minValue}");
                    }
                }
            }

            return minValue;
        }
    }
}