#!/usr/bin/env python3
"""
Final fix for the missing add_decision and add_objective methods
"""

import os
os.chdir("/Users/sumitm1/contextkeeper-pro-v3/contextkeeper")

# Read the file
with open("rag_agent.py", "r") as f:
    lines = f.readlines()

# Find the malformed method and replace it
in_malformed_method = False
replacement_start = -1
replacement_end = -1

for i, line in enumerate(lines):
    if "async def interactive_mode(self):" in line and "if decision_obj and project_id" in lines[i+2]:
        # This is the malformed method in ProjectKnowledgeAgent class (not RAGCLI)
        replacement_start = i
        in_malformed_method = True
        print(f"Found malformed method at line {i+1}")
        
    elif in_malformed_method and line.strip() == "return decision_obj":
        replacement_end = i + 1  # Include this line
        print(f"Found method end at line {i+1}")
        break

if replacement_start == -1 or replacement_end == -1:
    print("❌ Could not find the malformed method to replace")
    exit(1)

# Create the replacement methods
replacement_methods = [
    "    def add_decision(self, decision: str, reasoning: str = \"\", project_id: str = None, tags: List[str] = None) -> Optional[Any]:\n",
    "        \"\"\"Add a decision to a project with embedding/search functionality\"\"\"\n",
    "        try:\n",
    "            # Use focused project if no project_id provided\n",
    "            if project_id is None:\n",
    "                project_id = self.project_manager.focused_project_id\n",
    "                if not project_id:\n",
    "                    logger.error(\"No project specified and no focused project available\")\n",
    "                    return None\n",
    "            \n",
    "            # Validate project exists\n",
    "            if project_id not in self.project_manager.projects:\n",
    "                logger.error(f\"Project {project_id} not found\")\n",
    "                return None\n",
    "            \n",
    "            # Use project manager to create and persist the decision\n",
    "            decision_obj = self.project_manager.add_decision(\n",
    "                project_id=project_id,\n",
    "                decision=decision,\n",
    "                reasoning=reasoning,\n",
    "                tags=tags or []\n",
    "            )\n",
    "            \n",
    "            if decision_obj and project_id in self.collections:\n",
    "                # Create content for embedding\n",
    "                content = f\"PROJECT DECISION: {decision}\"\n",
    "                if reasoning:\n",
    "                    content += f\"\\nREASONING: {reasoning}\"\n",
    "                if tags:\n",
    "                    content += f\"\\nTAGS: {', '.join(tags)}\"\n",
    "                content += f\"\\nDATE: {decision_obj.timestamp}\"\n",
    "                \n",
    "                # Store decision in ChromaDB for embedding/search functionality\n",
    "                self.collections[project_id].add(\n",
    "                    ids=[decision_obj.id],\n",
    "                    documents=[content],\n",
    "                    metadatas=[{\n",
    "                        'type': 'decision',\n",
    "                        'project_id': project_id,\n",
    "                        'tags': tags or [],\n",
    "                        'date': decision_obj.timestamp\n",
    "                    }]\n",
    "                )\n",
    "                \n",
    "                logger.info(f\"Added decision to project {project_id}: {decision[:50]}...\")\n",
    "            \n",
    "            return decision_obj\n",
    "            \n",
    "        except Exception as e:\n",
    "            logger.error(f\"Error adding decision: {e}\")\n",
    "            return None\n",
    "    \n",
    "    def add_objective(self, title: str, description: str = \"\", priority: str = \"medium\", project_id: str = None) -> Optional[Any]:\n",
    "        \"\"\"Add an objective to a project with embedding/search functionality\"\"\"\n",
    "        try:\n",
    "            # Use focused project if no project_id provided\n",
    "            if project_id is None:\n",
    "                project_id = self.project_manager.focused_project_id\n",
    "                if not project_id:\n",
    "                    logger.error(\"No project specified and no focused project available\")\n",
    "                    return None\n",
    "            \n",
    "            # Validate project exists\n",
    "            if project_id not in self.project_manager.projects:\n",
    "                logger.error(f\"Project {project_id} not found\")\n",
    "                return None\n",
    "            \n",
    "            # Use project manager to create and persist the objective\n",
    "            objective_obj = self.project_manager.add_objective(\n",
    "                project_id=project_id,\n",
    "                title=title,\n",
    "                description=description,\n",
    "                priority=priority\n",
    "            )\n",
    "            \n",
    "            if objective_obj and project_id in self.collections:\n",
    "                # Create content for embedding\n",
    "                content = f\"PROJECT OBJECTIVE: {title}\"\n",
    "                if description:\n",
    "                    content += f\"\\nDESCRIPTION: {description}\"\n",
    "                content += f\"\\nPRIORITY: {priority}\"\n",
    "                content += f\"\\nDATE: {objective_obj.created_at}\"\n",
    "                \n",
    "                # Store objective in ChromaDB for embedding/search functionality\n",
    "                self.collections[project_id].add(\n",
    "                    ids=[objective_obj.id],\n",
    "                    documents=[content],\n",
    "                    metadatas=[{\n",
    "                        'type': 'objective',\n",
    "                        'project_id': project_id,\n",
    "                        'priority': priority,\n",
    "                        'date': objective_obj.created_at\n",
    "                    }]\n",
    "                )\n",
    "                \n",
    "                logger.info(f\"Added objective to project {project_id}: {title}\")\n",
    "            \n",
    "            return objective_obj\n",
    "            \n",
    "        except Exception as e:\n",
    "            logger.error(f\"Error adding objective: {e}\")\n",
    "            return None\n"
]

# Replace the malformed method with proper methods
new_lines = lines[:replacement_start] + replacement_methods + lines[replacement_end:]

# Write the fixed file
with open("rag_agent.py", "w") as f:
    f.writelines(new_lines)

print("✅ Successfully fixed rag_agent.py!")
print(f"✅ Replaced malformed method (lines {replacement_start+1}-{replacement_end})")
print("✅ Added proper add_decision and add_objective methods to ProjectKnowledgeAgent class")

# Verify the fix
with open("rag_agent.py", "r") as f:
    content = f.read()
    
if "def add_decision(self, decision: str" in content:
    print("✅ add_decision method successfully added")
else:
    print("❌ add_decision method not found after fix")

if "def add_objective(self, title: str" in content:
    print("✅ add_objective method successfully added")
else:
    print("❌ add_objective method not found after fix")

if "async def interactive_mode(self):" in content and "if decision_obj and project_id" in content:
    print("❌ Malformed method still exists")
else:
    print("✅ Malformed method successfully removed")

print("\n🎉 Fix complete! The Flask endpoints should now work properly.")