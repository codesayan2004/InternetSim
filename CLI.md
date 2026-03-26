# InternetSim CLI User Manual

## Overview

The **InternetSim CLI** allows users to Simulate Internet-scale BGP routing with support for:

- Loading AS topology and configuration files
- Announcing prefixes from ASes
- Modifying routing and non-BGP policies
- Running simulations and checking convergence
- Querying routes stored at specific ASes

> **Note:** All commands must end with a semicolon (`;`) unless inside a multiline policy block.

---

## Starting the CLI

Run the CLI from your terminal:

```bash
python3 cli.py
```

You will see the prompt:

```
Welcome to InternetSim CLI
>
```

---

## Available Commands

### 1. Load a File

Load any configuration file, such as AS relationships, ROV sets, or description files.

```
load <Key> = <FilePath>;
```

**Examples:**

```
load ASRelFilePath = data/20240501.as-rel.txt;
load ROVSetFilePath = data/rov_highdeg_10.txt;
load descriptionFilePath = description/mydesc.txt;
```

> After loading a file, you must run `init;` or `reload;` to apply changes.

---

### 2. Initialize or Reload Engine

Initialize the simulation engine:

```
init;
```

Reload topology or configuration files (preserves state):

```
reload;
```

---

### 3. BGP Announcements

Announce a prefix from a specific AS:

```
AS <ASN> announce <Prefix>;
```

**Examples:**

```
AS 174 announce 187.156.112.0/23;
AS 209 announce 149.181.128.0/20;
```

After announcements, run the simulation:

```
Simulate;
```

**Simulation output includes:**

| Field | Description |
|---|---|
| Convergence time | Time taken for BGP to converge |
| BGP updates | Number of BGP update messages |
| Affected ASes | Number of ASes affected by the announcement |

---

### 4. Query Routes

Check routes stored at an AS for a specific prefix:

```
AS <ASN> show routes <Prefix>;
```

**Example:**

```
AS 34549 show routes 29.214.0.0/16;
```

**Output lists all routes with:**

| Field | Description |
|---|---|
| `prefix` | The announced IP prefix |
| `origin` | Originating AS |
| `localPref` | Local preference value |
| `ASPath` | Full AS path |
| `community` | BGP community attributes |

---

### 5. Change Routing Policy *(Multiline)*

Modify routing policies for AS peers. A block starts with `Change routing policy:`.

**Syntax:**

```
Change routing policy:
AS <ASN> peer AS <ASN>
    filter in | filter out
        add rule | remove rule <id>
            match "<condition>"
            action "<action>"
        end
    end
end;
```

**Example:**

```
Change routing policy:
AS 34549 peer AS 1299
    filter in
        add rule
            match "prefix is 29.214.0.0/16"
            action "local-pref 200"
        end
    end
end;
```

**Commands inside the block:**

| Command | Description |
|---|---|
| `AS <ASN> peer AS <ASN>` | Target a peering relationship |
| `filter in` / `filter out` | Apply to inbound or outbound routes |
| `add rule` | Add a new routing rule |
| `remove rule <id>` | Remove an existing rule by ID |
| `match "<prefix>"` | Condition to match on |
| `action "<value>"` | Action to apply (e.g., `local-pref`, `NH`) |
| `end` | Close a rule, filter, or peer block |

> **Important:** The block must end with `end;`.

---

### 6. Change Non-BGP Policy *(Multiline)*

Enable or disable ROV (Route Origin Validation) at specific ASes:

**Syntax:**

```
Change non-BGP policy:
AS <ASN> enable ROV
...
end;
```

**Example:**

```
Change non-BGP policy:
AS 20473 enable ROV
AS 52025 enable ROV
end;
```

> **Important:** The block must end with `end;`.

---

### 7. Simulate

Run BGP simulation and update all routes:

```
Simulate;
```

**Output includes:**

- Convergence time
- BGP updates
- Number of affected ASes

---

### 8. Exit CLI

```
exit;
```

Closes the CLI safely.

---

## Notes & Tips

- Every command **outside** a multiline block must end with `;`.
- Multiline blocks do **not** require `;` inside — only `end;` to finish.
- Always run `init;` or `reload;` after loading a new file.
- You can run multiple policy changes and simulations iteratively.
- Invalid lines or commands will be rejected with a descriptive error message.


## Warning

If you run 
```
ROVSetFilePath = data/rov_highdeg_10.txt
```
Then 'reload;' wont help because we need to construct entire topology for this (as per simulator design)
So apply 'init;'. Hence all previous announcements will be lost.

## Example Session

Below is a typical session demonstrating the CLI workflow:

```text
$ python3 cli.py
Welcome to InternetSim CLI

> load ASRelFilePath = data/20240501.as-rel.txt;
Loaded ASRelFilePath = data/20240501.as-rel.txt
⚠️ Use init; or reload;

> load InvalidSetFilePath = data/Invalid-Set.txt;
Loaded InvalidSetFilePath = data/Invalid-Set.txt
⚠️ Use init; or reload;

> init;
Loaded 76802 ASes, 495579 links
Loaded 1 Invalid-SET
Engine initialized

> AS 174 announce 187.156.112.0/23;
> AS 209 announce 149.181.128.0/20;
> AS 286 announce 29.214.0.0/16;
> AS 1239 announce 186.80.0.0/13;
> AS 1299 announce 128.126.128.0/18;
> Simulate;
Simulation start
Simulation complete
Convergence time: 5.654624 seconds
BGP updates: 1366320
Affected ASes: 76228

> AS 34549 show routes 29.214.0.0/16;
AS 34549's route to 29.214.0.0/16:
Route(prefix=29.214.0.0/16, origin=IGP, localPref=60, ASPath=3223 1299 286, community=)
Route(prefix=29.214.0.0/16, origin=IGP, localPref=120, ASPath=3356 286, community=)

> Change routing policy:
AS 34549 peer AS 3356
    filter in
        add rule
            match "prefix is 29.214.0.0/16"
            action "local-pref 120"
        end
    end
end;
AS 34549 peer AS 3356 filter in rule 0: match "prefix is 29.214.0.0/16", action "local-pref 120"
Simulation start
Simulation complete
Convergence time: 0.001209 seconds
BGP updates: 73
Affected ASes: 60

> AS 34549 show routes 29.214.0.0/16;
AS 34549's route to 29.214.0.0/16:
Route(prefix=29.214.0.0/16, origin=IGP, localPref=120, ASPath=3356 286, community=)
Route(prefix=29.214.0.0/16, origin=IGP, localPref=60, ASPath=3223 1299 286, community=)

> AS 52866 announce 187.156.112.139/23;
> AS 8309 announce 187.156.112.139/23;
> Simulate;
Simulation start
Simulation complete
Convergence time: 0.988843 seconds
BGP updates: 530088
Affected ASes: 76382

> Change non-BGP policy:
AS 20473 enable ROV
AS 52025 enable ROV
AS 6939 enable ROV
end;
Simulation start
Simulation complete
Convergence time: 1.670786 seconds
BGP updates: 767772
Affected ASes: 71589

> AS 28223 show routes 187.156.112.139/23;
AS 28223's route to 187.156.112.139/23:
Route(prefix=187.156.112.139/23, origin=IGP, localPref=80, ASPath=37721 37008 25818 ..., community=)

> exit;
Exiting...