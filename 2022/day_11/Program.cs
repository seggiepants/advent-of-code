using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{
    public class Monkey
    {
        public decimal id {get; set;}
        public List<decimal> items {get; set;}
        public string num1 {get; set;}
        public string op {get; set;}
        public string num2 {get; set;}
        public decimal divisor {get; set;}
        public decimal monkeyTrue {get; set;}
        public decimal monkeyFalse {get; set;}
        public decimal inspectCount {get; set;}

        public Monkey()
        {
            Reset();
        }

        public void Reset()
        {
            items = new();
            num1 = "";
            num2 = "";
            op = "";
            divisor = 1;
            monkeyTrue = 0;
            monkeyFalse = 0;
            inspectCount = 0;
        }

        public override String ToString()
        {
            StringBuilder sb = new();
            sb.Append($"Monkey #{id}\n");
            sb.Append($"- Items: {String.Join(',', items)}\n");
            sb.Append($"- Next: {num1} {op} {num2}\n");
            sb.Append($"- Test = Divisible By {divisor}\n");
            sb.Append($"- If Test == True Then {monkeyTrue} else {monkeyFalse}\n");
            sb.Append($"- Inspected: {inspectCount}.");
            return sb.ToString();
        }
    }

    public class day_11
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

            // Part 1
            List<Monkey> data = Load(inputPath);
            Console.WriteLine(Part1(data));

            // Part 2
            data = Load(inputPath); // We mutated the data. Will be lazy and reload instead of trying to keep a copy around.
            Console.WriteLine(Part2(data));

            return 0;
        }

        static List<Monkey> Load(String path)
        {
            Regex header = new Regex(@"Monkey (?'id'\d+):", RegexOptions.Compiled);
            Regex items = new Regex(@"Starting items: (?'items'[\d+(, )?]+)", RegexOptions.Compiled);
            Regex operation = new Regex(@"Operation: new = (?'num1'old|\d+) (?'op'\+|\*|-|/) (?'num2'old|\d+)", RegexOptions.Compiled);
            Regex divisibleBy = new Regex(@"Test: divisible by (?'amt'\d+)", RegexOptions.Compiled);
            Regex conditionTrue = new Regex(@"If true: throw to monkey (?'id'\d+)", RegexOptions.Compiled);
            Regex conditionFalse = new Regex(@"If false: throw to monkey (?'id'\d+)", RegexOptions.Compiled);
            List<Monkey> data = new();

            int lineNum = 0;
            Monkey currentMonkey = null;

            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (header.IsMatch(line))
                {
                    MatchCollection matches = header.Matches(line);
                    foreach(Match match in matches)
                    {
                        GroupCollection groups = match.Groups;    
                        if (!Int32.TryParse(groups["id"].Value, out int id))
                        {
                            Console.WriteLine($"Error Parsing Monkey Header for line #{lineNum}: {line}.");
                            break;
                        }
                        currentMonkey = new Monkey();
                        currentMonkey.id = id;
                        data.Add(currentMonkey);
                    }                    
                }
                else if(items.IsMatch(line))
                {
                    if (currentMonkey != null)
                    {
                        MatchCollection matches = items.Matches(line);
                        foreach(Match match in matches)
                        {
                            GroupCollection groups = match.Groups;    
                            string[] itemList = groups["items"].Value.Trim().Split(',');
                            foreach(string item in itemList)
                            {
                                if (!Int32.TryParse(item.Trim(), out int itemNum))
                                {
                                    Console.WriteLine($"Error parsing {item} as a number on line #{lineNum}: {line}.");
                                    break;
                                }
                                currentMonkey.items.Add(itemNum);
                            }
                        }
                    }                    
                }
                else if(operation.IsMatch(line))
                {
                    if (currentMonkey != null)
                    {
                        MatchCollection matches = operation.Matches(line);
                        // num1 op num2
                        foreach(Match match in matches)
                        {
                            GroupCollection groups = match.Groups;    
                            currentMonkey.num1 = groups["num1"].Value.Trim();
                            currentMonkey.num2 = groups["num2"].Value.Trim();
                            currentMonkey.op = groups["op"].Value.Trim();
                        }
                    }                    
                }
                else if(divisibleBy.IsMatch(line))
                {
                    if (currentMonkey != null)
                    {
                        MatchCollection matches = divisibleBy.Matches(line);
                        // num1 op num2
                        foreach(Match match in matches)
                        {
                            GroupCollection groups = match.Groups;
                            if (!Int32.TryParse(groups["amt"].Value, out int amt))
                            {
                                Console.WriteLine($"Error Parsing Monkey Divisible By for line #{lineNum}: {line}.");
                                break;
                            }

                            currentMonkey.divisor = amt;
                        }
                    }                    
                }
                else if(conditionTrue.IsMatch(line))
                {
                    if (currentMonkey != null)
                    {
                        MatchCollection matches = conditionTrue.Matches(line);
                        // num1 op num2
                        foreach(Match match in matches)
                        {
                            GroupCollection groups = match.Groups;
                            if (!Int32.TryParse(groups["id"].Value, out int id))
                            {
                                Console.WriteLine($"Error Parsing Monkey True Target for line #{lineNum}: {line}.");
                                break;
                            }
                            currentMonkey.monkeyTrue = id;
                        }
                    }                    
                }
                else if(conditionFalse.IsMatch(line))
                {
                    if (currentMonkey != null)
                    {
                        MatchCollection matches = conditionFalse.Matches(line);
                        // num1 op num2
                        foreach(Match match in matches)
                        {
                            GroupCollection groups = match.Groups;
                            if (!Int32.TryParse(groups["id"].Value, out int id))
                            {
                                Console.WriteLine($"Error Parsing Monkey False Target for line #{lineNum}: {line}.");
                                break;
                            }
                            currentMonkey.monkeyFalse = id;
                        }
                    }                    
                }
            }
            return data;
        }

        static void PrintData(List<Monkey> data)
        {
            foreach(Monkey monkey in data)
            {
                Console.WriteLine(monkey.ToString());
            }
        }

        static decimal Simulate(List<Monkey> data, int numRounds, int worryDivisor)
        {
            // Make sure inspect count = 0 for each item first.
            // Also, don't let the amounts get out of range.
            // Product of all divisors should keep accuracy but
            // contain the worry levels.
            decimal controlFactor = 1m;
            foreach(Monkey monkey in data)
            {
                monkey.inspectCount = 0;
                controlFactor *= monkey.divisor;
            }
            
            // Repeat for desired number of rounds.
            for(int round = 0; round < numRounds; ++round)
            {
                // Every monkey in the group takes a turn.
                foreach(Monkey monkey in data)
                {
                    // Inspect while you have items to look at.
                    while (monkey.items.Count > 0)
                    {
                        // Pop off the first item in the item list.
                        decimal worryLevel = monkey.items[0];
                        monkey.items.RemoveAt(0);
                        monkey.inspectCount++;

                        // Compute new value. old = current worry level, otherwise a numeric constant.
                        decimal num1, num2;
                        if (monkey.num1.Equals("old"))
                        {
                            num1 = worryLevel;
                        }
                        else if (!decimal.TryParse(monkey.num1, out num1))
                        {
                            Console.WriteLine($"Error parsing first number in operation \"{monkey.num1}\".");
                            return -1;
                        }

                        if (monkey.num2.Equals("old"))
                        {
                            num2 = worryLevel;
                        }
                        else if (!decimal.TryParse(monkey.num2, out num2))
                        {
                            Console.WriteLine($"Error parsing second number in operation \"{monkey.num2}\".");
                            return -1;
                        }

                        decimal result = 0;
                        if (monkey.op == "+")
                        {
                            result = num1 + num2;
                        }
                        else if (monkey.op == "-")
                        {
                            result = num1 - num2;                            
                        }
                        else if (monkey.op == "*")
                        {
                            result = num1 * num2;                            
                        }
                        else if (monkey.op == "/")
                        {
                            result = num1 / num2;
                        }
                        else
                        {
                            Console.WriteLine($"Unsupported operator in operation \"{monkey.op}\".");
                            return -1;                            
                        }        

                        result = Math.Floor(result / worryDivisor);   
                        result = result % controlFactor; // controlFactor keeps worry levels reasonable without changing results.

                        // send item to target monkey
                        decimal targetMonkey = result % monkey.divisor == 0 ? monkey.monkeyTrue : monkey.monkeyFalse;
                        Monkey target = data.Find(x => x.id == targetMonkey);
                        target.items.Add(result);
                    }
                }
            }

            // Sort by number of inspections.
            var top = 
                from monkey in data 
                orderby monkey.inspectCount descending
                select monkey.inspectCount
                ;
            
            // Multiply top N together.
            decimal finalResult = 1;
            foreach(decimal amt in top.Take(2))
            {
                finalResult *= amt;
            }
            return finalResult;
        }

        static decimal Part1(List<Monkey> data)
        {
            return Simulate(data, 20, 3);
        }

        static decimal Part2(List<Monkey> data)
        {   
            return Simulate(data, 10000, 1);
        }
    }
}