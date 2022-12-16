using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{

    public class day_15
    {
        public static int Main(string[] args)
        {
            string inputPath = "sample_input.txt";
            if (args.Length > 0)
            {
                inputPath = args[0];
            }

            if (!File.Exists(inputPath))
            {
                Console.WriteLine($"Error: File Not Found \"{inputPath}\"");
                return -1;
            }

            List<Tuple<int, int, int, int>> data = Load(inputPath);            
            // PrintData(data);

            int minX = Int32.MaxValue;
            int minY = Int32.MaxValue;
            int maxX = Int32.MinValue;
            int maxY = Int32.MinValue;
            int x1 = 0, y1 = 0, x2 = 20, y2 = 20;

            Bounds(data, ref minX, ref minY, ref maxX, ref maxY);
            Console.WriteLine($"Bounds: ({minX}, {minY})-({maxX}, {maxY})");
            int sampleRow = 10;
            if (Distance(minX, minY, maxX, maxY) > 100)
            {
                sampleRow = 2000000;
                x2 = 4000000;
                y2 = 4000000;
            }

            // Part 1
            Console.WriteLine(Part1(data, sampleRow));            

            // Part 2
            Console.WriteLine(Part2(data, x1,y1, x2, y2));

            return 0;
        }

        static List<Tuple<int, int, int, int>> Load(String path)
        {
            List<Tuple<int, int, int, int>> data = new();
            Regex sensorLine = new Regex(@"Sensor at x=(?'sx'-?\d+), y=(?'sy'-?\d+): closest beacon is at x=(?'bx'-?\d+), y=(?'by'-?\d+)", RegexOptions.Compiled);
            int lineNum = 0;

            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (line.Length > 0)
                {                    
                    if (sensorLine.IsMatch(line))
                    {
                        MatchCollection matches = sensorLine.Matches(line);
                        foreach(Match match in matches)
                        {
                            GroupCollection groups = match.Groups;    
                            if (!Int32.TryParse(groups["sx"].Value, out int sx))
                            {
                                Console.WriteLine($"Error Parsing Sensor.x for line #{lineNum}: {line}.");
                                break;
                            }
                            if (!Int32.TryParse(groups["sy"].Value, out int sy))
                            {
                                Console.WriteLine($"Error Parsing Sensor.y for line #{lineNum}: {line}.");
                                break;
                            }
                            if (!Int32.TryParse(groups["bx"].Value, out int bx))
                            {
                                Console.WriteLine($"Error Parsing Beacon.x for line #{lineNum}: {line}.");
                                break;
                            }
                            if (!Int32.TryParse(groups["by"].Value, out int by))
                            {
                                Console.WriteLine($"Error Parsing Beacon.y for line #{lineNum}: {line}.");
                                break;
                            }                            
                            data.Add(new Tuple<int, int, int, int>(sx, sy, bx, by));
                        } // match
                    } // is match?
                } // line not empty.
            } // row in input
            return data;
        }

        static void Bounds(List<Tuple<int, int, int, int>> data, ref int minX, ref int minY, ref int maxX, ref int maxY)
        {
            minX = Int32.MaxValue;
            minY = Int32.MaxValue;
            maxX = Int32.MinValue;
            maxY = Int32.MinValue;

            foreach(Tuple<int, int, int, int> row in data)
            {
                int dist = Distance(row.Item1, row.Item2, row.Item3, row.Item4);

                minX = Math.Min(minX, row.Item1 -dist);
                minY = Math.Min(minY, row.Item2 - dist);
                maxX = Math.Max(maxX, row.Item1 + dist);
                maxY = Math.Max(maxY, row.Item2 + dist);

                /*
                minX = Math.Min(minX, row.Item3);
                minY = Math.Min(minY, row.Item4);
                maxX = Math.Max(maxX, row.Item3);
                maxY = Math.Max(maxY, row.Item4);
                */
            }
        }

        static int Distance(int x1, int y1, int x2, int y2)
        {
            return Math.Abs(x2 - x1) + Math.Abs(y2 - y1); // Manhattan Distance.
        }

        static void PrintData(List<Tuple<int, int, int, int>> data)
        {
            int minX = Int32.MaxValue;
            int minY = Int32.MaxValue;
            int maxX = Int32.MinValue;
            int maxY = Int32.MinValue;

            Bounds(data, ref minX, ref minY, ref maxX, ref maxY);

            HashSet<Tuple<int, int>> sensors = new();
            HashSet<Tuple<int, int>> beacons = new();
            foreach(Tuple<int, int, int, int> row in data)
            {
                Console.WriteLine($"Sensor ({row.Item1},{row.Item2}) - Beacon({row.Item3},{row.Item4})");
                Tuple<int, int> sensor = new(row.Item1, row.Item2);
                Tuple<int, int> beacon = new(row.Item3, row.Item4);
                sensors.Add(sensor);
                beacons.Add(beacon);
            }

            for (int y = minY; y <= maxY; ++ y)
            {
                for(int x = minX; x <= maxX; ++x)
                {
                    Tuple<int, int> point = new(x, y);
                    if (sensors.Contains(point))
                    {
                        Console.Write("S");
                    }
                    else if (beacons.Contains(point))
                    {
                        Console.Write("B");
                    }
                    else
                    {
                        Console.Write(".");
                    }
                }
                Console.WriteLine("");
            }
            Console.WriteLine("");
        }

        private static long TuningFrequency(long x, long y)
        {
            return (x * 4000000) + y;
        }
        static int Part1(List<Tuple<int, int, int, int>> data, int sampleRow)
        {
            /*
            int minX = Int32.MaxValue;
            int minY = Int32.MaxValue;
            int maxX = Int32.MinValue;
            int maxY = Int32.MinValue;

            Bounds(data, ref minX, ref minY, ref maxX, ref maxY);
            */
            /*            
            int numExcluded = 0;            
            for (int col = minX; col <= maxX;col++)
            {                    
                foreach(Tuple<int, int, int, int> sensor in data)
                {
                    int sensorX = sensor.Item1, sensorY = sensor.Item2, beaconX = sensor.Item3, beaconY = sensor.Item4;
                    int sensor2Beacon = Distance(sensorX, sensorY, beaconX, beaconY);
                    int sensor2Point = Distance(sensorX, sensorY, col, sampleRow);
                    if (sensor2Point <= sensor2Beacon)
                    {
                        numExcluded++;
                        break;
                    }
                }
            }
            */
            // Calc range reflected on a line for each sensor.
            HashSet<int> exclude = new();
            foreach(Tuple<int, int, int, int> sensor in data)
            {
                int sensorX = sensor.Item1, sensorY = sensor.Item2, beaconX = sensor.Item3, beaconY = sensor.Item4;
                int sensor2Beacon = Distance(sensorX, sensorY, beaconX, beaconY);
                int dy = Math.Abs(sensorY - sampleRow);
                if (dy > sensor2Beacon)
                    continue;
                int dx = sensor2Beacon - dy;
                //Console.WriteLine($"({sensorX - dx},{sampleRow})-({sensorX + dx},{sampleRow})");
                for(int x = sensorX - dx; x <= sensorX + dx; ++x)
                    exclude.Add(x);
            }

            foreach(Tuple<int, int, int, int> sensor in data)
            {
                int sensorX = sensor.Item1, sensorY = sensor.Item2, beaconX = sensor.Item3, beaconY = sensor.Item4;
                if (beaconY == sampleRow)
                    exclude.Remove(beaconX);

                if (sensorY == sampleRow)
                    exclude.Remove(sensorX);
            }

            // 3909635 is too low
            // 4985194 is too high.
            return exclude.Count;
        }

        static long Part2(List<Tuple<int, int, int, int>> data, int minX, int minY, int maxX, int maxY)
        {
            HashSet<Tuple<int, int>> beacons = new();
            HashSet<Tuple<int, int>> sensors = new();
            List<Tuple<int, int, int>>sensorDist = new();
            foreach(Tuple<int, int, int, int> sensor in data)
            {
                sensors.Add(new Tuple<int, int>(sensor.Item1, sensor.Item2));
                beacons.Add(new Tuple<int, int>(sensor.Item3, sensor.Item4));
                sensorDist.Add(new Tuple<int, int, int>(sensor.Item1, sensor.Item2, Distance(sensor.Item1, sensor.Item2, sensor.Item3, sensor.Item4)));
            }


            for(int y = minY; y <= maxY;++y)
            {
                if (y > 0 && y % 10000 == 0)
                    Console.Write(".");
                // Calc range reflected on a line for each sensor.
                List<Tuple<int, int>>ranges = new();

                foreach(Tuple<int, int, int> sensor in sensorDist)
                {
                    int sensorX = sensor.Item1, sensorY = sensor.Item2, dist = sensor.Item3;
                    int dy = Math.Abs(sensorY - y);
                    if (dy > dist)
                        continue;
                    int dx = dist - dy;
                    ranges.Add(new Tuple<int, int>(sensorX - dx, sensorX + dx));
                }

                ranges.Sort();
                // Look for something with a space inbetween.
                int currentMax = ranges[0].Item2;
                for (int i = 0; i < ranges.Count - 1; ++i)
                {
                    if ((ranges[i + 1].Item1 == ranges[i].Item2 + 2) && (ranges[i+1].Item1 > currentMax))
                    {
                        // Hole found.
                        Tuple<int, int> point = new(ranges[i].Item2 + 1, y);
                        if (!beacons.Contains(point) && !sensors.Contains(point))
                        {
                            Console.WriteLine($"x = {ranges[i].Item2 + 1}, y = {y}");
                            bool ok = true;
                            foreach(Tuple<int, int, int>check in sensorDist)
                            {
                                int dist1 = Distance(check.Item1, check.Item2, ranges[i].Item2 + 1, y);
                                if (dist1 <= check.Item3)
                                {
                                    ok = false;
                                    break;
                                }
                            }
                            if (ok)
                                return TuningFrequency((long)ranges[i].Item2 + 1, (long)y);
                        }
                    }
                    currentMax = Math.Max(currentMax, ranges[i].Item2);
                } 
            }
            // 355804606 IS TOO LOW
            return 0L;
        }
   }
}