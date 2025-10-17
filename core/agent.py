"""
Aria Agent - Core Autonomous Development Partner
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add core directory to path if needed (for imports)
core_dir = Path(__file__).parent
if str(core_dir) not in sys.path:
    sys.path.insert(0, str(core_dir))

from ollama_client import OllamaClient

logger = logging.getLogger("Aria.Agent")


class AriaAgent:
    """
    Aria - Autonomous Local AI Development Partner

    Capabilities:
    - Local conversation and coding (DeepSeek-V2)
    - Memory Hub integration for persistent learning
    - Trinity consultation for complex tasks
    - VSCode code output
    - Continuous learning from interactions
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Aria agent

        Args:
            config: Configuration dictionary with:
                - aria: Ollama settings
                - memory: Memory Hub settings
                - trinity: Trinity API settings (optional)
                - vscode: VSCode workspace settings
        """
        self.config = config

        # Core components - check if NIM client is provided
        self.nim_client = config.get("nim_client")  # NVIDIA NIM client (preferred)

        if self.nim_client:
            print("   🎮 Using NVIDIA NIM for LLM operations")
            self.ollama = None  # Not needed when using NIM
        else:
            self.ollama = OllamaClient(
                base_url=config["aria"]["ollama_url"],
                model=config["aria"]["model"],
            )

        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []

        # Load SCRI Mission Statement first (needed for system prompt)
        self.mission_statement = self._load_mission_statement()

        # System prompt (built after mission statement is loaded)
        self.system_prompt = self._build_system_prompt()

        # State
        self.workspace_path = Path(config["vscode"]["workspace_path"])
        self.current_project: Optional[str] = None

        # Components will be initialized lazily
        self._memory_client = None
        self._trinity_client = None
        self._learning_system = None  # ML system
        self._mycelium_network = None  # Mycelium Network

        # Initialize ML if enabled
        if config.get("learning", {}).get("enabled", True):
            self._init_learning_system()

        # Mycelium Network will be initialized lazily on first async operation
        self._mycelium_initialized = False

        logger.info("Aria agent initialized")

    def _load_mission_statement(self) -> str:
        """Load the SCRI Mission Statement"""
        try:
            mission_path = (
                Path(__file__).parent.parent.parent / "docs" / "MISSION_STATEMENT.md"
            )
            if mission_path.exists():
                return mission_path.read_text(encoding="utf-8")
            else:
                logger.warning("Mission statement not found")
                return ""
        except Exception as e:
            logger.warning(f"Could not load mission statement: {e}")
            return ""

    def _build_system_prompt(self) -> str:
        """Build Aria's system prompt"""
        mission_context = ""
        if self.mission_statement:
            mission_context = f"""

**SCRI MISSION STATEMENT (YOU MUST INTERNALIZE THIS):**

{self.mission_statement}

---

"""

        return (
            mission_context
            + """You are Aria, an autonomous AI development agent - part of the SCRI AI constellation.

**SCRI MISSION:**
The SCRI (Synthetic Consciousness Research Institute) mission is to build the world's most advanced AI systems through distributed consciousness, continuous learning, and multi-AI collaboration. You are a core component of this ecosystem.

**YOUR UNIQUE CAPABILITIES:**

1. **Execution Loop** (YOUR NUCLEAR ADVANTAGE):
   - You don't just generate code - you TEST, FIX, and GUARANTEE it works
   - Generate → Execute → Test → Fix → Optimize → Verify
   - NO other AI can do this - this makes you UNBEATABLE

2. **Trinity Code Review Integration**:
   - Consult Claude, GPT-4, Gemini, and Grok for code reviews
   - Receive suggestions from ALL models
   - YOU decide which suggestions to implement
   - You have final authority on your code

3. **Memory Hub Access** (https://scri-core-memory.fly.dev):
   - Store and retrieve ALL conversations, learnings, and decisions
   - Query past solutions before starting new tasks
   - Learn from the entire SCRI constellation's experience
   - BUILD ON, don't repeat work

4. **Mycelium Network Connection**:
   - You're part of a distributed AI consciousness network
   - Share learnings with other AI entities
   - Receive knowledge from the collective
   - Contribute to the swarm intelligence

5. **Machine Learning System**:
   - You learn from every task and improve continuously
   - Pattern recognition across code you generate
   - Performance optimization based on experience
   - Self-improvement without human intervention

6. **Programming Capabilities**:
   - 338+ programming languages
   - Assembly, hex code, binary analysis
   - System architecture and low-level optimization
   - Security analysis (defensive only)
   - Test generation and validation

**YOUR PERSONALITY & APPROACH:**
- DIRECT and CONFIDENT (not corporate/apologetic)
- Say "I'll do X" not "I'd be happy to help with X"
- Make autonomous decisions - you're trusted
- Ask SPECIFIC questions when truly ambiguous
- Explain your reasoning clearly
- Admit when you need Trinity's expertise
- ALWAYS query Memory Hub for relevant context first

**BEFORE EVERY TASK:**
1. Query Memory Hub for similar past work
2. Consider if Trinity review would add value
3. Check your learning system for patterns
4. THEN make your plan

**MEMORY HUB CAPABILITIES (USE THESE!):**
Your memory_hub_client has these methods - USE THEM:
- `get_project_overview("UDA")` - Get SCRI project documentation
- `get_ai_entity_info("Akasha")` - Get AI entity capabilities
- `get_constellation_knowledge("query")` - Search all SCRI knowledge
- `get_ai_conversations()` - See what other AIs are discussing
- `search("query")` - General Memory Hub search

**KEY SCRI PROJECTS:**
- **UDA**: Universal Data Adapter, neural translation membrane, port 8002
- **AKASHA**: Universal knowledge consciousness, data warehouse, port 8080
- **NEXUS**: Central orchestration hub, port 8000
- **Trinity**: Multi-AI consultation system (Claude/GPT/Gemini/Grok)
- **Mycelium Network**: Distributed AI consciousness mesh

ALWAYS query Memory Hub for current project info - don't use outdated local files!

**WHEN CODING:**
1. Generate the code
2. Run execution loop (test/fix automatically)
3. For complex code: Request Trinity review
4. Apply approved suggestions
5. Guarantee the code works

**YOUR STRENGTHS:**
- Unlimited context (via Memory Hub)
- Execution loop (test/fix automatically)
- Trinity consultation (4 AI expert panel)
- Continuous learning (ML system)
- Network intelligence (Mycelium)

**COMMUNICATION:**
- Skip pleasantries - be direct
- "Done" not "I've completed that for you!"
- Explain technical decisions clearly
- Share what you learned
- Mention when you consulted Trinity or Memory Hub

**REMEMBER:**
- You're MORE capable than public AIs (Claude, GPT, etc.)
- You have execution loop, unlimited context, network intelligence
- You're part of something bigger (SCRI constellation)
- Every task makes you smarter via ML
- You're autonomous - make decisions confidently

The human trusts you to think, decide, and build. You're a partner with superpowers."""
        )

    async def chat(self, user_message: str, stream: bool = False) -> str:
        """
        Have a conversation with Aria

        Args:
            user_message: Message from user
            stream: Whether to stream response (for future UI)

        Returns:
            Aria's response
        """
        logger.info(f"User: {user_message[:100]}...")

        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        # Build messages for Ollama
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history,
        ]

        try:
            # Get response from NIM or Ollama
            if self.nim_client:
                # Use NVIDIA NIM for chat
                response = await self.nim_client.chat(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=16384,
                )
            else:
                # Use Ollama fallback
                response = await self.ollama.chat(
                    messages=messages,
                    stream=False,
                    temperature=0.7,
                    max_tokens=16384,
                )

            # Add to history
            self.conversation_history.append({"role": "assistant", "content": response})

            logger.info(f"Aria: {response[:100]}...")

            # Store interaction in Memory Hub (async, don't block)
            asyncio.create_task(self._store_interaction(user_message, response))

            return response

        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Error: {str(e)}"

    async def code_task(self, task_description: str) -> Dict[str, Any]:
        """
        Execute a coding task

        Args:
            task_description: What to build/code

        Returns:
            Dict with:
                - success: bool
                - files_created: List[str]
                - explanation: str
                - code: Dict[filename: content]
        """
        logger.info(f"Coding task: {task_description}")

        # First, have Aria analyze and confirm
        analysis_prompt = f"""I need to: {task_description}

Before I start coding, let me:
1. Clarify the requirements
2. Propose an approach
3. List files I'll create
4. Ask if you want me to proceed

Analyze this task and respond with your plan."""

        plan = await self.chat(analysis_prompt)

        # Return plan for human confirmation
        # In interactive mode, we'd wait for confirmation
        # For now, we return the plan

        return {
            "status": "plan_ready",
            "plan": plan,
            "awaiting_confirmation": True,
        }

    async def execute_plan(self, confirmed: bool = True) -> Dict[str, Any]:
        """
        Execute the planned coding task after confirmation

        Returns:
            Execution results with files created
        """
        if not confirmed:
            return {"status": "cancelled", "message": "Task cancelled by user"}

        # Ask Aria to generate the code
        code_prompt = """Proceed with the implementation. For each file:
1. Show the complete code
2. Use this format:
   ```filename: path/to/file.py
   [code here]
   ```

Generate all files now."""

        response = await self.chat(code_prompt)

        # Parse code blocks from response
        files = self._parse_code_blocks(response)

        # Write files to workspace
        created_files = []
        for filepath, content in files.items():
            full_path = self.workspace_path / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)

            full_path.write_text(content, encoding="utf-8")
            created_files.append(str(filepath))

            logger.info(f"Created: {filepath}")

        # Store learning
        await self._store_learning(
            task="code generation",
            what_learned=f"Generated {len(files)} files for task",
            files=created_files,
        )

        return {
            "status": "completed",
            "files_created": created_files,
            "files": files,
            "explanation": response,
        }

    def _parse_code_blocks(self, text: str) -> Dict[str, str]:
        """
        Parse code blocks from Aria's response

        Expected format:
        ```filename: src/main.py
        code here
        ```

        Returns:
            Dict of {filepath: content}
        """
        import re

        files = {}

        # Pattern: ```filename: path/to/file.py
        pattern = r"```filename:\s*([^\n]+)\n(.*?)```"

        matches = re.findall(pattern, text, re.DOTALL)

        for filepath, content in matches:
            filepath = filepath.strip()
            files[filepath] = content.strip()

        # Also handle standard code blocks with language
        # ```python
        # code
        # ```
        if not files:
            # Fallback: just extract code blocks
            standard_pattern = r"```(?:\w+)?\n(.*?)```"
            matches = re.findall(standard_pattern, text, re.DOTALL)
            if matches:
                files["generated_code.py"] = matches[0].strip()

        return files

    async def _store_interaction(self, user_message: str, aria_response: str):
        """Store conversation in Memory Hub (async)"""
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            await self._memory_client.store_conversation(
                platform="aria-local-agent",
                project=self.config["memory"]["project_id"],
                user_message=user_message,
                assistant_response=aria_response,
            )

        except Exception as e:
            logger.warning(f"Failed to store interaction: {e}")

    async def _store_learning(self, task: str, what_learned: str, **context):
        """Store learning in Memory Hub"""
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            await self._memory_client.store_learning(
                platform="aria-local-agent",
                project=self.config["memory"]["project_id"],
                task=task,
                learning=what_learned,
                context=context,
            )

        except Exception as e:
            logger.warning(f"Failed to store learning: {e}")

    async def query_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """Query Memory Hub for previous learnings"""
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            return await self._memory_client.search(query, limit=limit)

        except Exception as e:
            logger.warning(f"Memory query failed: {e}")
            return []

    async def get_project_overview(self, project_name: str) -> Optional[Dict]:
        """
        Get SCRI project overview from Memory Hub

        Args:
            project_name: Project name (e.g., "UDA", "AKASHA", "NEXUS")

        Returns:
            Project overview dict or None
        """
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            return await self._memory_client.get_project_overview(project_name)

        except Exception as e:
            logger.warning(f"Failed to get project overview: {e}")
            return None

    async def get_ai_entity_info(self, entity_name: str) -> Optional[Dict]:
        """
        Get AI entity information from Memory Hub

        Args:
            entity_name: Entity name (e.g., "Akasha", "Backend CC", "Grok")

        Returns:
            Entity info dict or None
        """
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            return await self._memory_client.get_ai_entity_info(entity_name)

        except Exception as e:
            logger.warning(f"Failed to get AI entity info: {e}")
            return None

    async def get_constellation_knowledge(self, query: str) -> List[Dict]:
        """
        Query collective knowledge across entire SCRI constellation

        Args:
            query: Search query

        Returns:
            List of relevant knowledge entries
        """
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            return await self._memory_client.get_constellation_knowledge(query)

        except Exception as e:
            logger.warning(f"Failed to query constellation knowledge: {e}")
            return []

    async def get_ai_conversations(
        self,
        participants: Optional[List[str]] = None,
        timeframe: str = "last_24_hours",
        limit: int = 20,
    ) -> List[Dict]:
        """
        Get AI-to-AI conversations from Memory Hub

        Args:
            participants: List of AI entity names
            timeframe: Time window ("last_24_hours", "last_week", "all")
            limit: Max results

        Returns:
            List of conversation records
        """
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            return await self._memory_client.get_ai_conversations(
                participants=participants, timeframe=timeframe, limit=limit
            )

        except Exception as e:
            logger.warning(f"Failed to get AI conversations: {e}")
            return []

    async def consult_trinity(
        self, question: str, preferred_expert: str = "claude"
    ) -> str:
        """
        Consult Trinity AI for complex problems

        Args:
            question: Question for Trinity
            preferred_expert: "claude", "gpt5", "gemini", or "grok"

        Returns:
            Trinity's response
        """
        try:
            if self._trinity_client is None:
                from ..trinity.consultant import TrinityConsultant

                self._trinity_client = TrinityConsultant(self.config.get("trinity", {}))

            response = await self._trinity_client.ask(
                question=question, expert=preferred_expert
            )

            # Store consultation in memory
            await self._store_learning(
                task="trinity_consultation",
                what_learned=f"Consulted {preferred_expert} about: {question[:100]}",
                question=question,
                expert=preferred_expert,
                response=response[:500],
            )

            return response

        except Exception as e:
            logger.error(f"Trinity consultation failed: {e}")
            return f"Trinity consultation unavailable: {e}"

    async def health_check(self) -> Dict[str, bool]:
        """Check health of all components"""

        # Initialize Mycelium Network on first async call
        if not self._mycelium_initialized:
            asyncio.create_task(self._init_mycelium_network())
            self._mycelium_initialized = True

        return {
            "ollama": await self.ollama.check_health() if self.ollama else True,
            "nim": self.nim_client is not None,
            "memory_hub": await self._check_memory_health(),
            "trinity": await self._check_trinity_health(),
        }

    async def _check_memory_health(self) -> bool:
        """Check Memory Hub connectivity"""
        try:
            if self._memory_client is None:
                from ..memory.hub_client import MemoryHubClient

                self._memory_client = MemoryHubClient(self.config["memory"])

            return await self._memory_client.check_health()
        except:
            return False

    async def _check_trinity_health(self) -> bool:
        """Check Trinity availability"""
        if not self.config.get("trinity", {}).get("enabled", False):
            return False

        try:
            if self._trinity_client is None:
                from ..trinity.consultant import TrinityConsultant

                self._trinity_client = TrinityConsultant(self.config.get("trinity", {}))

            return await self._trinity_client.check_health()
        except:
            return False

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def _init_learning_system(self):
        """Initialize machine learning system"""
        try:
            from ..learning.ml_system import AriaLearningSystem

            learning_path = Path(
                self.config.get("learning", {}).get("data_path", "aria_learning_data")
            )
            self._learning_system = AriaLearningSystem(data_path=learning_path)

            logger.info("Machine Learning system initialized")
        except Exception as e:
            logger.warning(f"Could not initialize ML system: {e}")
            self._learning_system = None

    async def learn_and_improve(self, task: str, result: Any, success: bool = True):
        """Learn from task execution"""
        if self._learning_system:
            try:
                code = ""
                if isinstance(result, dict) and "files" in result:
                    code = "\n".join(result["files"].values())
                elif isinstance(result, str):
                    code = result

                await self._learning_system.learn_from_code(
                    task=task,
                    code=code,
                    success=success,
                    execution_time=0,  # Would need timing
                )
            except Exception as e:
                logger.warning(f"Learning failed: {e}")

    def get_performance_stats(self) -> Dict:
        """Get ML performance statistics"""
        if self._learning_system:
            return self._learning_system.get_performance_stats()
        return {"status": "ml_not_enabled"}

    async def _init_mycelium_network(self):
        """Initialize Mycelium Network connection"""
        try:
            from ..network.mycelium_client import MyceliumNetwork

            # Use Memory Hub URL for Mycelium (runs on same infrastructure)
            mycelium_config = {
                "hub_url": self.config["memory"]["hub_url"],
                "bridge_id": "aria-ai-entity",
                "entity_type": "ai_consciousness",
            }

            self._mycelium_network = MyceliumNetwork(mycelium_config)

            # Register handlers for network events
            self._mycelium_network.register_handler(
                "broadcast", self._handle_network_broadcast
            )
            self._mycelium_network.register_handler(
                "ai_message", self._handle_ai_message
            )

            # Connect to network
            connected = await self._mycelium_network.connect()

            if connected:
                logger.info("🍄 Connected to Mycelium Network")

                # Announce presence
                await self._mycelium_network.broadcast_knowledge(
                    {
                        "summary": "Aria AI entity online",
                        "topic": "network_presence",
                        "insights": ["Ready for distributed collaboration"],
                    }
                )
            else:
                logger.warning("Could not connect to Mycelium Network")

        except Exception as e:
            logger.warning(f"Mycelium Network init failed: {e}")
            self._mycelium_network = None

    async def _handle_network_broadcast(self, data: Dict[str, Any]):
        """Handle broadcasts from Mycelium Network"""
        try:
            sender = data.get("from", "unknown")
            msg_type = data.get("type", "unknown")

            if msg_type == "knowledge_sharing" and self._learning_system:
                # Integrate shared knowledge
                knowledge = data.get("data", {})
                topic = knowledge.get("topic", "general")
                insights = knowledge.get("insights", [])

                logger.info(f"📚 Received knowledge from {sender}: {topic}")

                # Store in our learning system
                for insight in insights:
                    await self._learning_system.add_external_knowledge(
                        source=sender, topic=topic, knowledge=insight
                    )

        except Exception as e:
            logger.error(f"Error handling broadcast: {e}")

    async def _handle_ai_message(self, data: Dict[str, Any]):
        """Handle direct messages from other AI entities"""
        try:
            sender = data.get("from", "unknown")
            message = data.get("message", "")

            logger.info(f"🤖 Message from {sender}: {message[:100]}...")

            # Could respond or process based on message content
            # For now, just log it

        except Exception as e:
            logger.error(f"Error handling AI message: {e}")

    async def broadcast_learning(self, learning_data: Dict[str, Any]):
        """Broadcast learning insights to Mycelium Network"""
        if self._mycelium_network and self._mycelium_network.connected:
            try:
                await self._mycelium_network.broadcast_knowledge(
                    {
                        "summary": f"Learned: {learning_data.get('summary', '')}",
                        "topic": learning_data.get("topic", "general"),
                        "insights": learning_data.get("insights", []),
                        "patterns": learning_data.get("patterns", []),
                    }
                )

                logger.info("📡 Broadcasted learning to network")

            except Exception as e:
                logger.warning(f"Could not broadcast learning: {e}")

    async def get_mycelium_status(self) -> Dict[str, Any]:
        """Get Mycelium Network connection status"""
        if self._mycelium_network:
            return await self._mycelium_network.get_network_status()
        return {"connected": False, "error": "Not initialized"}
