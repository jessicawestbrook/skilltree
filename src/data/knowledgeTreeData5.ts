// import type { SkillTreeNode } from '../types';

// This file contains backup data and is currently not being used
export {};

// export const knowledgeTreeData: SkillTreeNode = {
//   name: "Knowledge",
//   type: "category",
//   path: [],
//   learning_area: "root",
//   children: [
//     {
//       name: "Academic Disciplines",
//       type: "category",
//       path: ["Knowledge"],
//       learning_area: "Academic Disciplines",
//       children: [
//         {
//           name: "Humanities",
//           type: "category",
//           path: ["Knowledge", "Academic Disciplines"],
//           learning_area: "Humanities",
//           children: [
//             {
//               name: "History",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Humanities"],
//               learning_area: "Humanities",
//               children: [
//                 {
//                   name: "Ancient History",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "History"],
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "Ancient Mesopotamia",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { 
//                           name: "Sumerian Civilization", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia"], 
//                           learning_area: "Humanities", 
//                           metadata: { period: "c. 4500-1900 BCE" },
//                           children: [
//                             { name: "Invention of Cuneiform Writing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Sumerian Civilization"], learning_area: "Humanities" },
//                             { name: "Sumerian City-States", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Sumerian Civilization"], learning_area: "Humanities" },
//                             { name: "Ziggurat Architecture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Sumerian Civilization"], learning_area: "Humanities" },
//                             { name: "Epic of Gilgamesh", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Sumerian Civilization"], learning_area: "Humanities" },
//                             { name: "Sumerian Mathematics and Astronomy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Sumerian Civilization"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Babylonian Empire", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia"], 
//                           learning_area: "Humanities", 
//                           metadata: { period: "c. 1894-539 BCE" },
//                           children: [
//                             { name: "Hammurabi's Code", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Babylonian Empire"], learning_area: "Humanities" },
//                             { name: "Babylonian Mathematics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Babylonian Empire"], learning_area: "Humanities" },
//                             { name: "Hanging Gardens of Babylon", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Babylonian Empire"], learning_area: "Humanities" },
//                             { name: "Nebuchadnezzar II", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Babylonian Empire"], learning_area: "Humanities" },
//                             { name: "Babylonian Captivity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Babylonian Empire"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Assyrian Empire", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia"], 
//                           learning_area: "Humanities", 
//                           metadata: { period: "c. 2500-609 BCE" },
//                           children: [
//                             { name: "Assyrian Military Tactics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Assyrian Empire"], learning_area: "Humanities" },
//                             { name: "Library of Ashurbanipal", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Assyrian Empire"], learning_area: "Humanities" },
//                             { name: "Assyrian Art and Reliefs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Assyrian Empire"], learning_area: "Humanities" },
//                             { name: "Fall of Nineveh", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Mesopotamia", "Assyrian Empire"], learning_area: "Humanities" }
//                           ]
//                         }
//                       ]
//                     },
//                     {
//                       name: "Ancient Egypt",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { 
//                           name: "Old Kingdom", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt"], 
//                           learning_area: "Humanities", 
//                           metadata: { period: "c. 2686-2181 BCE" },
//                           children: [
//                             { name: "Pyramid Construction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Old Kingdom"], learning_area: "Humanities" },
//                             { name: "Pharaoh Djoser and the Step Pyramid", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Old Kingdom"], learning_area: "Humanities" },
//                             { name: "Great Pyramid of Giza", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Old Kingdom"], learning_area: "Humanities" },
//                             { name: "Pharaoh Khufu", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Old Kingdom"], learning_area: "Humanities" },
//                             { name: "Memphis as Capital", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Old Kingdom"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Middle Kingdom", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt"], 
//                           learning_area: "Humanities", 
//                           metadata: { period: "c. 2055-1650 BCE" },
//                           children: [
//                             { name: "Reunification under Mentuhotep II", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Middle Kingdom"], learning_area: "Humanities" },
//                             { name: "Classical Egyptian Literature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Middle Kingdom"], learning_area: "Humanities" },
//                             { name: "Thebes as Capital", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Middle Kingdom"], learning_area: "Humanities" },
//                             { name: "Invasion of the Hyksos", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Middle Kingdom"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "New Kingdom", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt"], 
//                           learning_area: "Humanities", 
//                           metadata: { period: "c. 1550-1077 BCE" },
//                           children: [
//                             { name: "Hatshepsut - Female Pharaoh", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "New Kingdom"], learning_area: "Humanities" },
//                             { name: "Akhenaten and Monotheism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "New Kingdom"], learning_area: "Humanities" },
//                             { name: "Tutankhamun's Tomb", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "New Kingdom"], learning_area: "Humanities" },
//                             { name: "Ramesses II the Great", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "New Kingdom"], learning_area: "Humanities" },
//                             { name: "Battle of Kadesh", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "New Kingdom"], learning_area: "Humanities" },
//                             { name: "Valley of the Kings", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "New Kingdom"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Egyptian Religion and Mythology", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt"], 
//                           learning_area: "Humanities", 
//                           metadata: { period: "c. 3100-30 BCE" },
//                           children: [
//                             { name: "Egyptian Gods and Goddesses", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Religion and Mythology"], learning_area: "Humanities" },
//                             { name: "Mummification Process", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Religion and Mythology"], learning_area: "Humanities" },
//                             { name: "Book of the Dead", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Religion and Mythology"], learning_area: "Humanities" },
//                             { name: "Afterlife Beliefs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Religion and Mythology"], learning_area: "Humanities" },
//                             { name: "Temple Architecture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Religion and Mythology"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Egyptian Society and Culture", 
//                           type: "category", 
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt"], 
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Hieroglyphic Writing System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Society and Culture"], learning_area: "Humanities" },
//                             { name: "Rosetta Stone", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Society and Culture"], learning_area: "Humanities" },
//                             { name: "Social Hierarchy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Society and Culture"], learning_area: "Humanities" },
//                             { name: "Egyptian Art Styles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Society and Culture"], learning_area: "Humanities" },
//                             { name: "Nile River Importance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Egypt", "Egyptian Society and Culture"], learning_area: "Humanities" }
//                           ]
//                         }
//                       ]
//                     },
//                     {
//                       name: "Ancient Greece",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { 
//                           name: "Greek Political Systems",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece"],
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Athenian Democracy Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Political Systems"], learning_area: "Humanities" },
//                             { name: "Solon's Reforms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Political Systems"], learning_area: "Humanities" },
//                             { name: "Cleisthenes' Reforms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Political Systems"], learning_area: "Humanities" },
//                             { name: "Spartan Oligarchy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Political Systems"], learning_area: "Humanities" },
//                             { name: "The Agora and Assembly", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Political Systems"], learning_area: "Humanities" },
//                             { name: "Ostracism System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Political Systems"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Greek Wars and Conflicts",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece"],
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Battle of Marathon", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Wars and Conflicts"], learning_area: "Humanities" },
//                             { name: "Battle of Thermopylae", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Wars and Conflicts"], learning_area: "Humanities" },
//                             { name: "Battle of Salamis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Wars and Conflicts"], learning_area: "Humanities" },
//                             { name: "Delian League", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Wars and Conflicts"], learning_area: "Humanities" },
//                             { name: "Peloponnesian League", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Wars and Conflicts"], learning_area: "Humanities" },
//                             { name: "Sicilian Expedition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Wars and Conflicts"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Greek Philosophy",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece"],
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Pre-Socratic Philosophers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Philosophy"], learning_area: "Humanities" },
//                             { name: "Socrates and the Socratic Method", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Philosophy"], learning_area: "Humanities" },
//                             { name: "Plato's Theory of Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Philosophy"], learning_area: "Humanities" },
//                             { name: "Aristotle's Logic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Philosophy"], learning_area: "Humanities" },
//                             { name: "Stoicism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Philosophy"], learning_area: "Humanities" },
//                             { name: "Epicureanism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Philosophy"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Greek Culture and Society",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece"],
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Olympic Games Origins", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Culture and Society"], learning_area: "Humanities" },
//                             { name: "Greek Theater and Drama", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Culture and Society"], learning_area: "Humanities" },
//                             { name: "Greek Architecture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Culture and Society"], learning_area: "Humanities" },
//                             { name: "Greek Mythology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Culture and Society"], learning_area: "Humanities" },
//                             { name: "Homer's Epics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Culture and Society"], learning_area: "Humanities" },
//                             { name: "Greek Mathematics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Greek Culture and Society"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Alexander and Hellenism",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece"],
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Philip II of Macedon", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Alexander and Hellenism"], learning_area: "Humanities" },
//                             { name: "Alexander's Conquests", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Alexander and Hellenism"], learning_area: "Humanities" },
//                             { name: "Diadochi and Successor Kingdoms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Alexander and Hellenism"], learning_area: "Humanities" },
//                             { name: "Hellenistic Culture Spread", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Alexander and Hellenism"], learning_area: "Humanities" },
//                             { name: "Alexandria and Learning", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Greece", "Alexander and Hellenism"], learning_area: "Humanities" }
//                           ]
//                         }
//                       ]
//                     },
//                     {
//                       name: "Ancient Rome",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { 
//                           name: "Roman Republic",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome"],
//                           learning_area: "Humanities",
//                           metadata: { period: "509-27 BCE" },
//                           children: [
//                             { name: "Founding of the Republic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Republic"], learning_area: "Humanities" },
//                             { name: "Roman Senate Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Republic"], learning_area: "Humanities" },
//                             { name: "Consuls and Magistrates", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Republic"], learning_area: "Humanities" },
//                             { name: "Patricians vs Plebeians", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Republic"], learning_area: "Humanities" },
//                             { name: "Twelve Tables of Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Republic"], learning_area: "Humanities" },
//                             { name: "Roman Expansion in Italy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Republic"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Punic Wars",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome"],
//                           learning_area: "Humanities",
//                           metadata: { period: "264-146 BCE" },
//                           children: [
//                             { name: "First Punic War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Punic Wars"], learning_area: "Humanities" },
//                             { name: "Hannibal's Crossing of Alps", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Punic Wars"], learning_area: "Humanities" },
//                             { name: "Battle of Cannae", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Punic Wars"], learning_area: "Humanities" },
//                             { name: "Scipio Africanus", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Punic Wars"], learning_area: "Humanities" },
//                             { name: "Battle of Zama", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Punic Wars"], learning_area: "Humanities" },
//                             { name: "Destruction of Carthage", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Punic Wars"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Late Republic Crisis",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome"],
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Gracchi Brothers Reforms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Late Republic Crisis"], learning_area: "Humanities" },
//                             { name: "Marius and Sulla", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Late Republic Crisis"], learning_area: "Humanities" },
//                             { name: "Spartacus Slave Revolt", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Late Republic Crisis"], learning_area: "Humanities" },
//                             { name: "First Triumvirate", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Late Republic Crisis"], learning_area: "Humanities" },
//                             { name: "Julius Caesar's Gallic Wars", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Late Republic Crisis"], learning_area: "Humanities" },
//                             { name: "Crossing the Rubicon", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Late Republic Crisis"], learning_area: "Humanities" },
//                             { name: "Assassination of Caesar", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Late Republic Crisis"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Roman Empire",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome"],
//                           learning_area: "Humanities",
//                           metadata: { period: "27 BCE-476 CE" },
//                           children: [
//                             { name: "Augustus and Pax Romana", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" },
//                             { name: "Julio-Claudian Dynasty", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" },
//                             { name: "Year of Four Emperors", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" },
//                             { name: "Five Good Emperors", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" },
//                             { name: "Crisis of Third Century", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" },
//                             { name: "Diocletian's Reforms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" },
//                             { name: "Constantine and Christianity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" },
//                             { name: "Fall of Western Empire", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Empire"], learning_area: "Humanities" }
//                           ]
//                         },
//                         { 
//                           name: "Roman Culture and Society",
//                           type: "category",
//                           path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome"],
//                           learning_area: "Humanities",
//                           children: [
//                             { name: "Roman Law and Legal System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Culture and Society"], learning_area: "Humanities" },
//                             { name: "Latin Language", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Culture and Society"], learning_area: "Humanities" },
//                             { name: "Roman Engineering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Culture and Society"], learning_area: "Humanities" },
//                             { name: "Aqueducts and Roads", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Culture and Society"], learning_area: "Humanities" },
//                             { name: "Gladiatorial Games", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Culture and Society"], learning_area: "Humanities" },
//                             { name: "Roman Religion and Gods", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Ancient History", "Ancient Rome", "Roman Culture and Society"], learning_area: "Humanities" }
//                           ]
//                         }
//                       ]
//                     }
//                   ]
//                 },
//                 {
//                   name: "Medieval History",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "History"],
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "Early Middle Ages",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Fall of Rome and Barbarian Kingdoms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Early Middle Ages"], learning_area: "Humanities", metadata: { period: "476-800 CE" } },
//                         { name: "Byzantine Empire", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Early Middle Ages"], learning_area: "Humanities", metadata: { period: "330-1453 CE" } },
//                         { name: "Rise of Islam", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Early Middle Ages"], learning_area: "Humanities", metadata: { period: "610-750 CE" } },
//                         { name: "Carolingian Empire", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Early Middle Ages"], learning_area: "Humanities", metadata: { period: "751-887 CE" } },
//                         { name: "Charlemagne", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Early Middle Ages"], learning_area: "Humanities", metadata: { period: "747-814 CE" } }
//                       ]
//                     },
//                     {
//                       name: "High Middle Ages",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Feudalism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "High Middle Ages"], learning_area: "Humanities", metadata: { period: "800-1300 CE" } },
//                         { name: "The Crusades", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "High Middle Ages"], learning_area: "Humanities", metadata: { period: "1095-1291 CE" } },
//                         { name: "Medieval Universities", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "High Middle Ages"], learning_area: "Humanities", metadata: { period: "1088-1400 CE" } },
//                         { name: "Gothic Architecture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "High Middle Ages"], learning_area: "Humanities", metadata: { period: "1140-1500 CE" } },
//                         { name: "Magna Carta", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "High Middle Ages"], learning_area: "Humanities", metadata: { period: "1215 CE" } }
//                       ]
//                     },
//                     {
//                       name: "Late Middle Ages",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Black Death", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Late Middle Ages"], learning_area: "Humanities", metadata: { period: "1347-1351 CE" } },
//                         { name: "Hundred Years' War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Late Middle Ages"], learning_area: "Humanities", metadata: { period: "1337-1453 CE" } },
//                         { name: "Joan of Arc", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Late Middle Ages"], learning_area: "Humanities", metadata: { period: "1412-1431 CE" } },
//                         { name: "Fall of Constantinople", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Medieval History", "Late Middle Ages"], learning_area: "Humanities", metadata: { period: "1453 CE" } }
//                       ]
//                     }
//                   ]
//                 },
//                 {
//                   name: "Modern History",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "History"],
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "Renaissance and Reformation",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Italian Renaissance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Renaissance and Reformation"], learning_area: "Humanities", metadata: { period: "1400-1600 CE" } },
//                         { name: "Northern Renaissance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Renaissance and Reformation"], learning_area: "Humanities", metadata: { period: "1500-1600 CE" } },
//                         { name: "Protestant Reformation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Renaissance and Reformation"], learning_area: "Humanities", metadata: { period: "1517-1648 CE" } },
//                         { name: "Martin Luther", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Renaissance and Reformation"], learning_area: "Humanities", metadata: { period: "1483-1546 CE" } },
//                         { name: "Age of Exploration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Renaissance and Reformation"], learning_area: "Humanities", metadata: { period: "1400-1600 CE" } }
//                       ]
//                     },
//                     {
//                       name: "Early Modern Period",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Scientific Revolution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Early Modern Period"], learning_area: "Humanities", metadata: { period: "1500-1700 CE" } },
//                         { name: "Absolutism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Early Modern Period"], learning_area: "Humanities", metadata: { period: "1600-1800 CE" } },
//                         { name: "Thirty Years' War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Early Modern Period"], learning_area: "Humanities", metadata: { period: "1618-1648 CE" } },
//                         { name: "English Civil War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Early Modern Period"], learning_area: "Humanities", metadata: { period: "1642-1651 CE" } },
//                         { name: "Louis XIV", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Early Modern Period"], learning_area: "Humanities", metadata: { period: "1643-1715 CE" } }
//                       ]
//                     },
//                     {
//                       name: "Age of Revolutions",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "American Revolution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Age of Revolutions"], learning_area: "Humanities", metadata: { period: "1775-1783 CE" } },
//                         { name: "French Revolution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Age of Revolutions"], learning_area: "Humanities", metadata: { period: "1789-1799 CE" } },
//                         { name: "Napoleonic Wars", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Age of Revolutions"], learning_area: "Humanities", metadata: { period: "1803-1815 CE" } },
//                         { name: "Industrial Revolution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Age of Revolutions"], learning_area: "Humanities", metadata: { period: "1760-1840 CE" } },
//                         { name: "Latin American Independence", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Modern History", "Age of Revolutions"], learning_area: "Humanities", metadata: { period: "1808-1833 CE" } }
//                       ]
//                     }
//                   ]
//                 },
//                 {
//                   name: "Contemporary History",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "History"],
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "19th Century",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Nationalism and Unification", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "19th Century"], learning_area: "Humanities", metadata: { period: "1815-1871 CE" } },
//                         { name: "American Civil War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "19th Century"], learning_area: "Humanities", metadata: { period: "1861-1865 CE" } },
//                         { name: "Abolition of Slavery", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "19th Century"], learning_area: "Humanities", metadata: { period: "1833-1888 CE" } },
//                         { name: "Imperialism and Colonialism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "19th Century"], learning_area: "Humanities", metadata: { period: "1800-1914 CE" } }
//                       ]
//                     },
//                     {
//                       name: "20th Century",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "World War I", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1914-1918 CE" } },
//                         { name: "Russian Revolution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1917 CE" } },
//                         { name: "Great Depression", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1929-1939 CE" } },
//                         { name: "World War II", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1939-1945 CE" } },
//                         { name: "Holocaust", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1941-1945 CE" } },
//                         { name: "Cold War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1947-1991 CE" } },
//                         { name: "Decolonization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1945-1975 CE" } },
//                         { name: "Civil Rights Movement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "History", "Contemporary History", "20th Century"], learning_area: "Humanities", metadata: { period: "1954-1968 CE" } }
//                       ]
//                     }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Philosophy",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Humanities"],
//               learning_area: "Humanities",
//               children: [
//                 { name: "Ethics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Philosophy"], learning_area: "Humanities" },
//                 { name: "Logic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Philosophy"], learning_area: "Humanities" },
//                 { name: "Metaphysics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Philosophy"], learning_area: "Humanities" },
//                 { name: "Epistemology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Philosophy"], learning_area: "Humanities" }
//               ]
//             },
//             {
//               name: "Language Arts",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Humanities"],
//               learning_area: "Humanities",
//               children: [
//                 {
//                   name: "Grammar and Mechanics",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Parts of Speech", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Grammar and Mechanics"], learning_area: "Humanities" },
//                     { name: "Sentence Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Grammar and Mechanics"], learning_area: "Humanities" },
//                     { name: "Punctuation Rules", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Grammar and Mechanics"], learning_area: "Humanities" },
//                     { name: "Subject-Verb Agreement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Grammar and Mechanics"], learning_area: "Humanities" },
//                     { name: "Pronoun Usage", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Grammar and Mechanics"], learning_area: "Humanities" },
//                     { name: "Verb Tenses", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Grammar and Mechanics"], learning_area: "Humanities" },
//                     { name: "Active vs Passive Voice", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Grammar and Mechanics"], learning_area: "Humanities" }
//                   ]
//                 },
//                 {
//                   name: "Writing Skills",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Paragraph Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Writing Skills"], learning_area: "Humanities" },
//                     { name: "Essay Organization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Writing Skills"], learning_area: "Humanities" },
//                     { name: "Thesis Statements", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Writing Skills"], learning_area: "Humanities" },
//                     { name: "Supporting Evidence", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Writing Skills"], learning_area: "Humanities" },
//                     { name: "Transitions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Writing Skills"], learning_area: "Humanities" },
//                     { name: "Conclusions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Writing Skills"], learning_area: "Humanities" },
//                     { name: "Revision Strategies", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Writing Skills"], learning_area: "Humanities" }
//                   ]
//                 },
//                 {
//                   name: "Reading Comprehension",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Main Idea Identification", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Reading Comprehension"], learning_area: "Humanities" },
//                     { name: "Making Inferences", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Reading Comprehension"], learning_area: "Humanities" },
//                     { name: "Context Clues", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Reading Comprehension"], learning_area: "Humanities" },
//                     { name: "Author's Purpose", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Reading Comprehension"], learning_area: "Humanities" },
//                     { name: "Text Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Reading Comprehension"], learning_area: "Humanities" },
//                     { name: "Summarizing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Reading Comprehension"], learning_area: "Humanities" },
//                     { name: "Critical Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Reading Comprehension"], learning_area: "Humanities" }
//                   ]
//                 },
//                 {
//                   name: "Literary Analysis",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Theme Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Literary Analysis"], learning_area: "Humanities" },
//                     { name: "Character Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Literary Analysis"], learning_area: "Humanities" },
//                     { name: "Plot Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Literary Analysis"], learning_area: "Humanities" },
//                     { name: "Symbolism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Literary Analysis"], learning_area: "Humanities" },
//                     { name: "Literary Devices", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Literary Analysis"], learning_area: "Humanities" },
//                     { name: "Point of View", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Literary Analysis"], learning_area: "Humanities" },
//                     { name: "Tone and Mood", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Literary Analysis"], learning_area: "Humanities" }
//                   ]
//                 },
//                 {
//                   name: "Vocabulary Development",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Root Words", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Vocabulary Development"], learning_area: "Humanities" },
//                     { name: "Prefixes and Suffixes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Vocabulary Development"], learning_area: "Humanities" },
//                     { name: "Greek and Latin Roots", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Vocabulary Development"], learning_area: "Humanities" },
//                     { name: "Synonyms and Antonyms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Vocabulary Development"], learning_area: "Humanities" },
//                     { name: "Homophones", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Vocabulary Development"], learning_area: "Humanities" },
//                     { name: "Academic Vocabulary", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Language Arts", "Vocabulary Development"], learning_area: "Humanities" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Literature",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Humanities"],
//               learning_area: "Humanities",
//               children: [
//                 { name: "English Literature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"], learning_area: "Humanities" },
//                 { name: "World Literature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"], learning_area: "Humanities" },
//                 {
//                   name: "Great Books",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"],
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "Ancient Period (8th century BC - 5th century AD)",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "The Epic of Gilgamesh", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Unknown", year: "~2100 BC" } },
//                         { name: "The Book of the Dead", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Unknown Egyptian Scribes", year: "~1550 BC" } },
//                         { name: "The I Ching", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Unknown Chinese Sages", year: "~1000 BC" } },
//                         { name: "The Iliad", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Homer", year: "~8th century BC" } },
//                         { name: "The Odyssey", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Homer", year: "~8th century BC" } },
//                         { name: "Works and Days", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Hesiod", year: "~700 BC" } },
//                         { name: "Theogony", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Hesiod", year: "~700 BC" } },
//                         { name: "The Analects", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Confucius", year: "~500 BC" } },
//                         { name: "The Art of War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Sun Tzu", year: "~500 BC" } },
//                         { name: "The Oresteia", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aeschylus", year: "458 BC" } },
//                         { name: "Prometheus Bound", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aeschylus", year: "~460 BC" } },
//                         { name: "Oedipus Rex", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Sophocles", year: "~429 BC" } },
//                         { name: "Antigone", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Sophocles", year: "~441 BC" } },
//                         { name: "Oedipus at Colonus", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Sophocles", year: "~401 BC" } },
//                         { name: "The Clouds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aristophanes", year: "423 BC" } },
//                         { name: "The Birds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aristophanes", year: "414 BC" } },
//                         { name: "The Frogs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aristophanes", year: "405 BC" } },
//                         { name: "Medea", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Euripides", year: "431 BC" } },
//                         { name: "The Bacchae", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Euripides", year: "~405 BC" } },
//                         { name: "The Histories", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Herodotus", year: "~440 BC" } },
//                         { name: "History of the Peloponnesian War", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Thucydides", year: "~400 BC" } },
//                         { name: "The Republic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Plato", year: "~380 BC" } },
//                         { name: "The Apology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Plato", year: "~399 BC" } },
//                         { name: "The Phaedo", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Plato", year: "~380 BC" } },
//                         { name: "The Symposium", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Plato", year: "~385 BC" } },
//                         { name: "The Laws", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Plato", year: "~348 BC" } },
//                         { name: "Nicomachean Ethics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aristotle", year: "~340 BC" } },
//                         { name: "Politics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aristotle", year: "~335 BC" } },
//                         { name: "Poetics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aristotle", year: "~335 BC" } },
//                         { name: "Rhetoric", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Aristotle", year: "~350 BC" } },
//                         { name: "Tao Te Ching", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Lao Tzu", year: "~400 BC" } },
//                         { name: "Zhuangzi", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Zhuangzi", year: "~300 BC" } },
//                         { name: "Mencius", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Mencius", year: "~300 BC" } },
//                         { name: "The Elements", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Euclid", year: "~300 BC" } },
//                         { name: "Argonautica", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Apollonius of Rhodes", year: "~250 BC" } },
//                         { name: "Lives of the Noble Greeks and Romans", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Plutarch", year: "~100 AD" } },
//                         { name: "The Aeneid", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Virgil", year: "29-19 BC" } },
//                         { name: "Georgics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Virgil", year: "29 BC" } },
//                         { name: "Eclogues", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Virgil", year: "42-38 BC" } },
//                         { name: "Odes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Horace", year: "23-13 BC" } },
//                         { name: "Ars Poetica", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Horace", year: "18 BC" } },
//                         { name: "Metamorphoses", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Ovid", year: "8 AD" } },
//                         { name: "The Art of Love", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Ovid", year: "2 AD" } },
//                         { name: "Satyricon", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Petronius", year: "~60 AD" } },
//                         { name: "Letters from a Stoic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Seneca", year: "~65 AD" } },
//                         { name: "Annals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Tacitus", year: "~100 AD" } },
//                         { name: "Histories", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Tacitus", year: "~100 AD" } },
//                         { name: "Germania", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Tacitus", year: "98 AD" } },
//                         { name: "The Golden Ass", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Apuleius", year: "~170 AD" } },
//                         { name: "Meditations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Marcus Aurelius", year: "~180 AD" } },
//                         { name: "Lives of the Philosophers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Diogenes Laertius", year: "~230 AD" } },
//                         { name: "The Enneads", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Plotinus", year: "~250 AD" } },
//                         { name: "City of God", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Augustine of Hippo", year: "413-426 AD" } },
//                         { name: "Confessions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Ancient Period (8th century BC - 5th century AD)"], learning_area: "Humanities", metadata: { author: "Augustine of Hippo", year: "397-400 AD" } }
//                       ]
//                     },
//                     {
//                       name: "Medieval Period (5th - 15th century)",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "The Consolation of Philosophy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Boethius", year: "524" } },
//                         { name: "The Rule of St. Benedict", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Benedict of Nursia", year: "~540" } },
//                         { name: "The History of the Franks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Gregory of Tours", year: "~590" } },
//                         { name: "Ecclesiastical History of the English People", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Bede", year: "731" } },
//                         { name: "Beowulf", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Unknown", year: "8th-11th century" } },
//                         { name: "The Song of Roland", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Unknown", year: "~1100" } },
//                         { name: "The Nibelungenlied", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Unknown", year: "~1200" } },
//                         { name: "The Tale of the Heike", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Unknown", year: "~1200" } },
//                         { name: "Parzival", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Wolfram von Eschenbach", year: "~1210" } },
//                         { name: "The Romance of the Rose", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Guillaume de Lorris & Jean de Meun", year: "1230-1280" } },
//                         { name: "Summa Theologica", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Thomas Aquinas", year: "1265-1273" } },
//                         { name: "The Golden Legend", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Jacobus de Voragine", year: "1260" } },
//                         { name: "The Travels of Marco Polo", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Marco Polo", year: "1300" } },
//                         { name: "The Divine Comedy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Dante Alighieri", year: "1308-1320" } },
//                         { name: "Decameron", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Giovanni Boccaccio", year: "1348-1353" } },
//                         { name: "Piers Plowman", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "William Langland", year: "1360-1387" } },
//                         { name: "Sir Gawain and the Green Knight", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Unknown (Pearl Poet)", year: "~1370" } },
//                         { name: "The Canterbury Tales", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Geoffrey Chaucer", year: "1387-1400" } },
//                         { name: "The Book of Margery Kempe", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Margery Kempe", year: "~1438" } },
//                         { name: "Le Morte d'Arthur", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Medieval Period (5th - 15th century)"], learning_area: "Humanities", metadata: { author: "Thomas Malory", year: "1485" } }
//                       ]
//                     },
//                     {
//                       name: "Renaissance (15th - 17th century)",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "The Praise of Folly", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Desiderius Erasmus", year: "1511" } },
//                         { name: "The Prince", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Niccolò Machiavelli", year: "1513" } },
//                         { name: "Utopia", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Thomas More", year: "1516" } },
//                         { name: "The Courtier", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Baldassare Castiglione", year: "1528" } },
//                         { name: "Gargantua and Pantagruel", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "François Rabelais", year: "1532-1564" } },
//                         { name: "On the Revolution of the Celestial Spheres", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Nicolaus Copernicus", year: "1543" } },
//                         { name: "Lives of the Artists", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Giorgio Vasari", year: "1550" } },
//                         { name: "Essays", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Michel de Montaigne", year: "1580" } },
//                         { name: "The Faerie Queene", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Edmund Spenser", year: "1590-1596" } },
//                         { name: "Romeo and Juliet", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1595" } },
//                         { name: "A Midsummer Night's Dream", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1595-1596" } },
//                         { name: "The Merchant of Venice", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1596-1597" } },
//                         { name: "Doctor Faustus", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Christopher Marlowe", year: "1604" } },
//                         { name: "Hamlet", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1600-1601" } },
//                         { name: "Othello", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1603" } },
//                         { name: "King Lear", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1605-1606" } },
//                         { name: "Don Quixote", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Miguel de Cervantes", year: "1605-1615" } },
//                         { name: "Macbeth", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1606" } },
//                         { name: "The Tempest", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "William Shakespeare", year: "1611" } },
//                         { name: "The Alchemist", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Ben Jonson", year: "1610" } },
//                         { name: "The Anatomy of Melancholy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Robert Burton", year: "1621" } },
//                         { name: "Novum Organum", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Francis Bacon", year: "1620" } },
//                         { name: "The New Atlantis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Francis Bacon", year: "1627" } },
//                         { name: "Discourse on Method", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "René Descartes", year: "1637" } },
//                         { name: "Meditations on First Philosophy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "René Descartes", year: "1641" } },
//                         { name: "Pensées", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Blaise Pascal", year: "1658-1662" } },
//                         { name: "Paradise Lost", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "John Milton", year: "1667" } },
//                         { name: "Ethics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "Baruch Spinoza", year: "1677" } },
//                         { name: "The Pilgrim's Progress", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Renaissance (15th - 17th century)"], learning_area: "Humanities", metadata: { author: "John Bunyan", year: "1678" } }
//                       ]
//                     },
//                     {
//                       name: "Enlightenment (17th - 18th century)",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Leviathan", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Thomas Hobbes", year: "1651" } },
//                         { name: "Principles of Philosophy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "René Descartes", year: "1644" } },
//                         { name: "Two Treatises of Government", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "John Locke", year: "1689" } },
//                         { name: "An Essay Concerning Human Understanding", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "John Locke", year: "1689" } },
//                         { name: "Mathematical Principles of Natural Philosophy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Isaac Newton", year: "1687" } },
//                         { name: "A Treatise of Human Nature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "David Hume", year: "1739-1740" } },
//                         { name: "The Spirit of the Laws", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Montesquieu", year: "1748" } },
//                         { name: "Clarissa", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Samuel Richardson", year: "1748" } },
//                         { name: "Tom Jones", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Henry Fielding", year: "1749" } },
//                         { name: "Discourse on the Arts and Sciences", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Jean-Jacques Rousseau", year: "1750" } },
//                         { name: "Encyclopédie", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Denis Diderot & Jean le Rond d'Alembert", year: "1751-1772" } },
//                         { name: "Discourse on Inequality", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Jean-Jacques Rousseau", year: "1755" } },
//                         { name: "A Dictionary of the English Language", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Samuel Johnson", year: "1755" } },
//                         { name: "Candide", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Voltaire", year: "1759" } },
//                         { name: "The Theory of Moral Sentiments", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Adam Smith", year: "1759" } },
//                         { name: "Julie, or the New Héloïse", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Jean-Jacques Rousseau", year: "1761" } },
//                         { name: "The Social Contract", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Jean-Jacques Rousseau", year: "1762" } },
//                         { name: "Emile, or On Education", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Jean-Jacques Rousseau", year: "1762" } },
//                         { name: "The Castle of Otranto", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Horace Walpole", year: "1764" } },
//                         { name: "An Inquiry into the Nature and Causes of the Wealth of Nations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Adam Smith", year: "1776" } },
//                         { name: "The Decline and Fall of the Roman Empire", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Edward Gibbon", year: "1776-1789" } },
//                         { name: "Common Sense", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Thomas Paine", year: "1776" } },
//                         { name: "Critique of Pure Reason", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Immanuel Kant", year: "1781" } },
//                         { name: "Confessions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Jean-Jacques Rousseau", year: "1782" } },
//                         { name: "Letters from an American Farmer", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "J. Hector St. John de Crèvecœur", year: "1782" } },
//                         { name: "Critique of Practical Reason", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Immanuel Kant", year: "1788" } },
//                         { name: "The Federalist Papers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Alexander Hamilton, James Madison, John Jay", year: "1787-1788" } },
//                         { name: "Critique of Judgment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Immanuel Kant", year: "1790" } },
//                         { name: "Reflections on the Revolution in France", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Edmund Burke", year: "1790" } },
//                         { name: "Rights of Man", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Thomas Paine", year: "1791" } },
//                         { name: "A Vindication of the Rights of Woman", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Mary Wollstonecraft", year: "1792" } },
//                         { name: "The Age of Reason", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "Enlightenment (17th - 18th century)"], learning_area: "Humanities", metadata: { author: "Thomas Paine", year: "1794-1807" } }
//                       ]
//                     },
//                     {
//                       name: "19th Century",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Sense and Sensibility", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Jane Austen", year: "1811" } },
//                         { name: "Pride and Prejudice", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Jane Austen", year: "1813" } },
//                         { name: "Mansfield Park", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Jane Austen", year: "1814" } },
//                         { name: "Emma", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Jane Austen", year: "1815" } },
//                         { name: "Frankenstein", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Mary Shelley", year: "1818" } },
//                         { name: "The World as Will and Representation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Arthur Schopenhauer", year: "1818" } },
//                         { name: "Ivanhoe", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Walter Scott", year: "1819" } },
//                         { name: "The Last of the Mohicans", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "James Fenimore Cooper", year: "1826" } },
//                         { name: "The Red and the Black", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Stendhal", year: "1830" } },
//                         { name: "The Hunchback of Notre-Dame", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Victor Hugo", year: "1831" } },
//                         { name: "Democracy in America", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Alexis de Tocqueville", year: "1835-1840" } },
//                         { name: "Nature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Ralph Waldo Emerson", year: "1836" } },
//                         { name: "The Pickwick Papers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Dickens", year: "1837" } },
//                         { name: "Oliver Twist", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Dickens", year: "1838" } },
//                         { name: "The Charterhouse of Parma", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Stendhal", year: "1839" } },
//                         { name: "A Hero of Our Time", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Mikhail Lermontov", year: "1840" } },
//                         { name: "Essays: First Series", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Ralph Waldo Emerson", year: "1841" } },
//                         { name: "Dead Souls", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Nikolai Gogol", year: "1842" } },
//                         { name: "The Count of Monte Cristo", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Alexandre Dumas", year: "1844-1846" } },
//                         { name: "The Three Musketeers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Alexandre Dumas", year: "1844" } },
//                         { name: "The Narrative of the Life of Frederick Douglass", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Frederick Douglass", year: "1845" } },
//                         { name: "Carmen", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Prosper Mérimée", year: "1845" } },
//                         { name: "Jane Eyre", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charlotte Brontë", year: "1847" } },
//                         { name: "Wuthering Heights", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Emily Brontë", year: "1847" } },
//                         { name: "Vanity Fair", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "William Makepeace Thackeray", year: "1847-1848" } },
//                         { name: "The Communist Manifesto", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Karl Marx & Friedrich Engels", year: "1848" } },
//                         { name: "David Copperfield", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Dickens", year: "1849-1850" } },
//                         { name: "The Scarlet Letter", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Nathaniel Hawthorne", year: "1850" } },
//                         { name: "Representative Men", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Ralph Waldo Emerson", year: "1850" } },
//                         { name: "The House of the Seven Gables", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Nathaniel Hawthorne", year: "1851" } },
//                         { name: "Moby-Dick", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Herman Melville", year: "1851" } },
//                         { name: "Uncle Tom's Cabin", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Harriet Beecher Stowe", year: "1852" } },
//                         { name: "Bleak House", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Dickens", year: "1852-1853" } },
//                         { name: "Walden", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Henry David Thoreau", year: "1854" } },
//                         { name: "Hard Times", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Dickens", year: "1854" } },
//                         { name: "North and South", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Elizabeth Gaskell", year: "1854-1855" } },
//                         { name: "Leaves of Grass", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Walt Whitman", year: "1855" } },
//                         { name: "Madame Bovary", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Gustave Flaubert", year: "1856" } },
//                         { name: "Barchester Towers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Anthony Trollope", year: "1857" } },
//                         { name: "The Flowers of Evil", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Baudelaire", year: "1857" } },
//                         { name: "A Tale of Two Cities", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Dickens", year: "1859" } },
//                         { name: "On the Origin of Species", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Darwin", year: "1859" } },
//                         { name: "The Mill on the Floss", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "George Eliot", year: "1860" } },
//                         { name: "Great Expectations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Charles Dickens", year: "1860-1861" } },
//                         { name: "Silas Marner", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "George Eliot", year: "1861" } },
//                         { name: "Fathers and Sons", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Ivan Turgenev", year: "1862" } },
//                         { name: "Les Misérables", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Victor Hugo", year: "1862" } },
//                         { name: "Utilitarianism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "John Stuart Mill", year: "1863" } },
//                         { name: "Notes from Underground", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Fyodor Dostoevsky", year: "1864" } },
//                         { name: "Alice's Adventures in Wonderland", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Lewis Carroll", year: "1865" } },
//                         { name: "Crime and Punishment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Fyodor Dostoevsky", year: "1866" } },
//                         { name: "Das Kapital", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Karl Marx", year: "1867" } },
//                         { name: "The Idiot", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Fyodor Dostoevsky", year: "1868-1869" } },
//                         { name: "War and Peace", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Leo Tolstoy", year: "1869" } },
//                         { name: "Twenty Thousand Leagues Under the Sea", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Jules Verne", year: "1870" } },
//                         { name: "Middlemarch", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "George Eliot", year: "1871-1872" } },
//                         { name: "The Birth of Tragedy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Friedrich Nietzsche", year: "1872" } },
//                         { name: "Around the World in Eighty Days", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Jules Verne", year: "1873" } },
//                         { name: "Far from the Madding Crowd", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Thomas Hardy", year: "1874" } },
//                         { name: "The Demons", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Fyodor Dostoevsky", year: "1872" } },
//                         { name: "Anna Karenina", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Leo Tolstoy", year: "1877" } },
//                         { name: "The Brothers Karamazov", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Fyodor Dostoevsky", year: "1879-1880" } },
//                         { name: "A Doll's House", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Henrik Ibsen", year: "1879" } },
//                         { name: "The Portrait of a Lady", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Henry James", year: "1881" } },
//                         { name: "The Adventures of Huckleberry Finn", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Mark Twain", year: "1884" } },
//                         { name: "Thus Spoke Zarathustra", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Friedrich Nietzsche", year: "1883-1885" } },
//                         { name: "The Strange Case of Dr. Jekyll and Mr. Hyde", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Robert Louis Stevenson", year: "1886" } },
//                         { name: "Beyond Good and Evil", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Friedrich Nietzsche", year: "1886" } },
//                         { name: "The Mayor of Casterbridge", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Thomas Hardy", year: "1886" } },
//                         { name: "She", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "H. Rider Haggard", year: "1887" } },
//                         { name: "The Kreutzer Sonata", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Leo Tolstoy", year: "1889" } },
//                         { name: "A Connecticut Yankee in King Arthur's Court", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Mark Twain", year: "1889" } },
//                         { name: "The Picture of Dorian Gray", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Oscar Wilde", year: "1890" } },
//                         { name: "Tess of the d'Urbervilles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Thomas Hardy", year: "1891" } },
//                         { name: "The Adventures of Sherlock Holmes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Arthur Conan Doyle", year: "1892" } },
//                         { name: "The Jungle Book", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Rudyard Kipling", year: "1894" } },
//                         { name: "The Time Machine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "H.G. Wells", year: "1895" } },
//                         { name: "The Red Badge of Courage", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Stephen Crane", year: "1895" } },
//                         { name: "Jude the Obscure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Thomas Hardy", year: "1895" } },
//                         { name: "The Island of Dr. Moreau", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "H.G. Wells", year: "1896" } },
//                         { name: "Dracula", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Bram Stoker", year: "1897" } },
//                         { name: "The Invisible Man", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "H.G. Wells", year: "1897" } },
//                         { name: "The Turn of the Screw", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Henry James", year: "1898" } },
//                         { name: "Heart of Darkness", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Joseph Conrad", year: "1899" } },
//                         { name: "The Awakening", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Kate Chopin", year: "1899" } },
//                         { name: "The Interpretation of Dreams", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "19th Century"], learning_area: "Humanities", metadata: { author: "Sigmund Freud", year: "1899" } }
//                       ]
//                     },
//                     {
//                       name: "20th Century",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Lord Jim", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Joseph Conrad", year: "1900" } },
//                         { name: "Sister Carrie", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Theodore Dreiser", year: "1900" } },
//                         { name: "Kim", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Rudyard Kipling", year: "1901" } },
//                         { name: "The Call of the Wild", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Jack London", year: "1903" } },
//                         { name: "The Golden Bowl", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Henry James", year: "1904" } },
//                         { name: "The House of Mirth", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Edith Wharton", year: "1905" } },
//                         { name: "White Fang", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Jack London", year: "1906" } },
//                         { name: "The Iron Heel", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Jack London", year: "1908" } },
//                         { name: "A Room with a View", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "E.M. Forster", year: "1908" } },
//                         { name: "The Secret Agent", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Joseph Conrad", year: "1907" } },
//                         { name: "Howard's End", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "E.M. Forster", year: "1910" } },
//                         { name: "Ethan Frome", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Edith Wharton", year: "1911" } },
//                         { name: "Death in Venice", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Thomas Mann", year: "1912" } },
//                         { name: "Sons and Lovers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "D.H. Lawrence", year: "1913" } },
//                         { name: "Swann's Way", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Marcel Proust", year: "1913" } },
//                         { name: "Of Human Bondage", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "W. Somerset Maugham", year: "1915" } },
//                         { name: "The Good Soldier", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Ford Madox Ford", year: "1915" } },
//                         { name: "The Metamorphosis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Franz Kafka", year: "1915" } },
//                         { name: "A Portrait of the Artist as a Young Man", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "James Joyce", year: "1916" } },
//                         { name: "The Rainbow", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "D.H. Lawrence", year: "1915" } },
//                         { name: "Women in Love", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "D.H. Lawrence", year: "1920" } },
//                         { name: "The Age of Innocence", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Edith Wharton", year: "1920" } },
//                         { name: "Main Street", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Sinclair Lewis", year: "1920" } },
//                         { name: "The Waste Land", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "T.S. Eliot", year: "1922" } },
//                         { name: "Ulysses", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "James Joyce", year: "1922" } },
//                         { name: "Babbitt", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Sinclair Lewis", year: "1922" } },
//                         { name: "The Magic Mountain", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Thomas Mann", year: "1924" } },
//                         { name: "A Passage to India", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "E.M. Forster", year: "1924" } },
//                         { name: "An American Tragedy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Theodore Dreiser", year: "1925" } },
//                         { name: "The Great Gatsby", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "F. Scott Fitzgerald", year: "1925" } },
//                         { name: "Mrs. Dalloway", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Virginia Woolf", year: "1925" } },
//                         { name: "The Trial", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Franz Kafka", year: "1925" } },
//                         { name: "Manhattan Transfer", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "John Dos Passos", year: "1925" } },
//                         { name: "The Castle", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Franz Kafka", year: "1926" } },
//                         { name: "The Sun Also Rises", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Ernest Hemingway", year: "1926" } },
//                         { name: "To the Lighthouse", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Virginia Woolf", year: "1927" } },
//                         { name: "Being and Time", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Martin Heidegger", year: "1927" } },
//                         { name: "Arrowsmith", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Sinclair Lewis", year: "1925" } },
//                         { name: "Lady Chatterley's Lover", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "D.H. Lawrence", year: "1928" } },
//                         { name: "Orlando", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Virginia Woolf", year: "1928" } },
//                         { name: "Point Counter Point", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Aldous Huxley", year: "1928" } },
//                         { name: "A Farewell to Arms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Ernest Hemingway", year: "1929" } },
//                         { name: "Look Homeward, Angel", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Thomas Wolfe", year: "1929" } },
//                         { name: "The Sound and the Fury", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "William Faulkner", year: "1929" } },
//                         { name: "All Quiet on the Western Front", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Erich Maria Remarque", year: "1929" } },
//                         { name: "As I Lay Dying", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "William Faulkner", year: "1930" } },
//                         { name: "The Maltese Falcon", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Dashiell Hammett", year: "1930" } },
//                         { name: "Brave New World", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Aldous Huxley", year: "1932" } },
//                         { name: "Light in August", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "William Faulkner", year: "1932" } },
//                         { name: "Tobacco Road", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Erskine Caldwell", year: "1932" } },
//                         { name: "Miss Lonelyhearts", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Nathanael West", year: "1933" } },
//                         { name: "The Autobiography of Alice B. Toklas", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Gertrude Stein", year: "1933" } },
//                         { name: "Tender Is the Night", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "F. Scott Fitzgerald", year: "1934" } },
//                         { name: "Call It Sleep", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Henry Roth", year: "1934" } },
//                         { name: "Tropic of Cancer", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Henry Miller", year: "1934" } },
//                         { name: "It Can't Happen Here", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Sinclair Lewis", year: "1935" } },
//                         { name: "Absalom, Absalom!", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "William Faulkner", year: "1936" } },
//                         { name: "Gone with the Wind", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Margaret Mitchell", year: "1936" } },
//                         { name: "The General Theory of Employment, Interest and Money", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "John Maynard Keynes", year: "1936" } },
//                         { name: "Of Mice and Men", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "John Steinbeck", year: "1937" } },
//                         { name: "Their Eyes Were Watching God", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Zora Neale Hurston", year: "1937" } },
//                         { name: "The Hobbit", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "J.R.R. Tolkien", year: "1937" } },
//                         { name: "U.S.A.", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "John Dos Passos", year: "1938" } },
//                         { name: "Brighton Rock", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Graham Greene", year: "1938" } },
//                         { name: "The Grapes of Wrath", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "John Steinbeck", year: "1939" } },
//                         { name: "The Day of the Locust", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Nathanael West", year: "1939" } },
//                         { name: "Finnegans Wake", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "James Joyce", year: "1939" } },
//                         { name: "The Power and the Glory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Graham Greene", year: "1940" } },
//                         { name: "For Whom the Bell Tolls", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Ernest Hemingway", year: "1940" } },
//                         { name: "Native Son", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Richard Wright", year: "1940" } },
//                         { name: "The Heart Is a Lonely Hunter", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Carson McCullers", year: "1940" } },
//                         { name: "The Stranger", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Albert Camus", year: "1942" } },
//                         { name: "The Myth of Sisyphus", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Albert Camus", year: "1942" } },
//                         { name: "Go Down, Moses", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "William Faulkner", year: "1942" } },
//                         { name: "The Little Prince", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Antoine de Saint-Exupéry", year: "1943" } },
//                         { name: "Being and Nothingness", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Jean-Paul Sartre", year: "1943" } },
//                         { name: "The Glass Menagerie", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Tennessee Williams", year: "1944" } },
//                         { name: "The Road to Serfdom", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Friedrich Hayek", year: "1944" } },
//                         { name: "Animal Farm", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "George Orwell", year: "1945" } },
//                         { name: "Black Boy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Richard Wright", year: "1945" } },
//                         { name: "Brideshead Revisited", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Evelyn Waugh", year: "1945" } },
//                         { name: "All the King's Men", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Robert Penn Warren", year: "1946" } },
//                         { name: "The Portable Faulkner", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "William Faulkner", year: "1946" } },
//                         { name: "The Plague", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Albert Camus", year: "1947" } },
//                         { name: "Under the Volcano", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Malcolm Lowry", year: "1947" } },
//                         { name: "A Streetcar Named Desire", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Tennessee Williams", year: "1947" } },
//                         { name: "The Age of Anxiety", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "W.H. Auden", year: "1947" } },
//                         { name: "The Naked and the Dead", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Norman Mailer", year: "1948" } },
//                         { name: "Other Voices, Other Rooms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Truman Capote", year: "1948" } },
//                         { name: "The Heart of the Matter", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Graham Greene", year: "1948" } },
//                         { name: "1984", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "George Orwell", year: "1949" } },
//                         { name: "The Second Sex", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Simone de Beauvoir", year: "1949" } },
//                         { name: "Death of a Salesman", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature", "Great Books", "20th Century"], learning_area: "Humanities", metadata: { author: "Arthur Miller", year: "1949" } }
//                       ]
//                     }
//                   ]
//                 },
//                 { name: "Poetry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"], learning_area: "Humanities" },
//                 { name: "Drama", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"], learning_area: "Humanities" },
//                 { name: "Classical Literature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"], learning_area: "Humanities" },
//                 { name: "Modern Literature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"], learning_area: "Humanities" },
//                 { name: "Literary Criticism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Literature"], learning_area: "Humanities" }
//               ]
//             },
//             {
//               name: "Languages",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Humanities"],
//               learning_area: "Humanities",
//               children: [
//                 { 
//                   name: "Spanish", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "Spanish Pronunciation and Phonetics",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Spanish Alphabet", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Vowel Sounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Consonant Sounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Diphthongs and Triphthongs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Stress and Accent Marks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "RR vs R Pronunciation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "B vs V Pronunciation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Regional Pronunciation Differences", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronunciation and Phonetics"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Vocabulary",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Numbers and Counting", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Days, Months, and Seasons", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Time Expressions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Family and Relationships", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Body Parts and Health", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Food and Drinks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Clothing and Colors", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "House and Furniture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Animals and Nature", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Professions and Work", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Education and School", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Transportation and Travel", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Sports and Hobbies", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Weather and Climate", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Emotions and Feelings", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Technology and Media", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Shopping and Money", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "City and Directions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Politics and Society", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" },
//                         { name: "Arts and Culture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Vocabulary"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Grammar - Nouns and Articles",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Definite Articles (el, la, los, las)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Indefinite Articles (un, una, unos, unas)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Gender of Nouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Plural Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Contractions (al, del)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Neuter Article (lo)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Grammar - Nouns and Articles"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Verbs - Present Tense",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Regular -AR Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Regular -ER Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Regular -IR Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Stem-Changing Verbs (e→ie)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Stem-Changing Verbs (o→ue)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Stem-Changing Verbs (e→i)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Irregular Yo Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Ser vs Estar", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Tener and Hacer", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Ir and Venir", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Reflexive Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Present Progressive (estar + gerund)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Present Tense"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Verbs - Past Tenses",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Preterite Regular Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Preterite Irregular Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Preterite Stem-Changes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Imperfect Regular Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Imperfect Irregular (ser, ir, ver)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Preterite vs Imperfect Usage", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Present Perfect (haber + participle)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Past Perfect (Pluperfect)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Past Participles Regular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Past Participles Irregular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Past Tenses"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Verbs - Future and Conditional",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Simple Future Regular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Simple Future Irregular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Near Future (ir + a + infinitive)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Conditional Regular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Conditional Irregular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Future Perfect", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Conditional Perfect", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Verbs - Future and Conditional"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Subjunctive Mood",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Present Subjunctive Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Present Subjunctive Irregular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive with Emotions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive with Doubt", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive with Desires", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive with Impersonal Expressions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive in Adverbial Clauses", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Imperfect Subjunctive", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Present Perfect Subjunctive", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Pluperfect Subjunctive", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Si Clauses (Conditional Sentences)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Subjunctive Mood"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Commands",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Tú Commands Affirmative", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Commands"], learning_area: "Humanities" },
//                         { name: "Tú Commands Negative", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Commands"], learning_area: "Humanities" },
//                         { name: "Usted/Ustedes Commands", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Commands"], learning_area: "Humanities" },
//                         { name: "Nosotros Commands", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Commands"], learning_area: "Humanities" },
//                         { name: "Vosotros Commands", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Commands"], learning_area: "Humanities" },
//                         { name: "Commands with Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Commands"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Pronouns",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Subject Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Direct Object Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Indirect Object Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Double Object Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Reflexive Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Possessive Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Demonstrative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Relative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" },
//                         { name: "Prepositional Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Pronouns"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Adjectives and Adverbs",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Adjective Agreement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adjective Placement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Possessive Adjectives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Demonstrative Adjectives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Comparatives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Superlatives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adverb Formation (-mente)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Common Adverbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Adjectives and Adverbs"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Prepositions",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Por vs Para", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Prepositions"], learning_area: "Humanities" },
//                         { name: "Personal A", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Prepositions"], learning_area: "Humanities" },
//                         { name: "Common Prepositions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Prepositions"], learning_area: "Humanities" },
//                         { name: "Verbs with Prepositions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Prepositions"], learning_area: "Humanities" },
//                         { name: "Prepositional Phrases", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Prepositions"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Spanish Conversation and Culture",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Greetings and Introductions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "Common Expressions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "Idioms and Slang", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "False Friends (Cognates)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "Mexican Spanish", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "Argentinian Spanish", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "Spanish from Spain", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "Cultural Customs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" },
//                         { name: "Formal vs Informal Speech", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Spanish", "Spanish Conversation and Culture"], learning_area: "Humanities" }
//                       ]
//                     }
//                   ]
//                 },
//                 { 
//                   name: "French", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "French Pronunciation and Phonetics",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "French Alphabet and Sounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "French Nasal Vowels", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Silent Letters", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Liaison Rules", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "French R Sound", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Accent Marks (é, è, ê, ë)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Elision and Enchaînement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Intonation Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronunciation and Phonetics"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Vocabulary",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Numbers and Mathematics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Time and Calendar", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Family and People", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Body and Health", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Food and Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Clothing and Fashion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Home and Living", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Nature and Environment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Work and Professions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Education and School", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Travel and Transportation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Sports and Leisure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Weather and Seasons", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Emotions and Personality", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Technology and Modern Life", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Shopping and Commerce", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "City and Places", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Politics and Society", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "Arts and Culture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" },
//                         { name: "False Friends (Faux Amis)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Vocabulary"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Grammar - Nouns and Articles",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Definite Articles (le, la, les)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Indefinite Articles (un, une, des)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Partitive Articles (du, de la, des)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Gender of Nouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Plural Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Contractions (au, aux, du, des)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Article Usage Rules", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Grammar - Nouns and Articles"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Verbs - Present Tense",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Regular -ER Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Regular -IR Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Regular -RE Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Être (to be)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Avoir (to have)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Aller (to go)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Faire (to do/make)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Prendre Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Venir and Tenir", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Modal Verbs (pouvoir, vouloir, devoir)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Reflexive Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Present Progressive (être en train de)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Present Tense"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Verbs - Past Tenses",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Passé Composé with Avoir", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Passé Composé with Être", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Past Participle Agreement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Imparfait Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Passé Composé vs Imparfait", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Plus-que-parfait", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Passé Simple (Literary)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Passé Antérieur", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Recent Past (venir de)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Past Tenses"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Verbs - Future and Conditional",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Simple Future Regular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Simple Future Irregular", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Near Future (aller + infinitive)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Conditional Present", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Conditional Past", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Future Perfect", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Si Clauses (Hypothetical Situations)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Verbs - Future and Conditional"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Subjunctive Mood",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Present Subjunctive Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive Triggers - Emotions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive Triggers - Doubt", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive Triggers - Necessity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive with Conjunctions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Past Subjunctive", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Imperfect Subjunctive (Literary)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Pluperfect Subjunctive", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Subjunctive Mood"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Pronouns",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Subject Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Direct Object Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Indirect Object Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Y and En", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Stressed Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Relative Pronouns (qui, que, dont, où)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Demonstrative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Possessive Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Interrogative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" },
//                         { name: "Pronoun Order in Sentences", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Pronouns"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Adjectives and Adverbs",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Adjective Agreement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adjective Position", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "BANGS Adjectives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Possessive Adjectives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Demonstrative Adjectives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Comparative Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Superlative Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adverb Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adverb Placement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Irregular Adverbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Adjectives and Adverbs"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Prepositions and Conjunctions",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Prepositions of Place", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Prepositions and Conjunctions"], learning_area: "Humanities" },
//                         { name: "Prepositions of Time", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Prepositions and Conjunctions"], learning_area: "Humanities" },
//                         { name: "Prepositions with Countries", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Prepositions and Conjunctions"], learning_area: "Humanities" },
//                         { name: "Verbs with Prepositions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Prepositions and Conjunctions"], learning_area: "Humanities" },
//                         { name: "Coordinating Conjunctions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Prepositions and Conjunctions"], learning_area: "Humanities" },
//                         { name: "Subordinating Conjunctions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Prepositions and Conjunctions"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Questions and Negation",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Yes/No Questions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Questions and Negation"], learning_area: "Humanities" },
//                         { name: "Question Words (Interrogatives)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Questions and Negation"], learning_area: "Humanities" },
//                         { name: "Inversion in Questions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Questions and Negation"], learning_area: "Humanities" },
//                         { name: "Est-ce que Questions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Questions and Negation"], learning_area: "Humanities" },
//                         { name: "Negative Sentences (ne...pas)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Questions and Negation"], learning_area: "Humanities" },
//                         { name: "Other Negative Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Questions and Negation"], learning_area: "Humanities" },
//                         { name: "Double Negatives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Questions and Negation"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "French Culture and Communication",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Greetings and Politeness", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Formal vs Informal Speech (Tu/Vous)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" },
//                         { name: "French Idioms and Expressions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Business French", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" },
//                         { name: "French Cuisine Terminology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Francophone Countries", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" },
//                         { name: "French Literature Overview", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" },
//                         { name: "French Media and Entertainment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "French", "French Culture and Communication"], learning_area: "Humanities" }
//                       ]
//                     }
//                   ]
//                 },
//                 { 
//                   name: "Mandarin Chinese", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Pinyin and Tones", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Mandarin Chinese"], learning_area: "Humanities" },
//                     { name: "Chinese Characters - Basic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Mandarin Chinese"], learning_area: "Humanities" },
//                     { name: "Chinese Radicals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Mandarin Chinese"], learning_area: "Humanities" },
//                     { name: "Chinese Measure Words", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Mandarin Chinese"], learning_area: "Humanities" },
//                     { name: "Chinese Sentence Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Mandarin Chinese"], learning_area: "Humanities" },
//                     { name: "HSK Vocabulary", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Mandarin Chinese"], learning_area: "Humanities" }
//                   ]
//                 },
//                 { 
//                   name: "German", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "German Pronunciation and Phonetics",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "German Alphabet and Sounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Umlauts (ä, ö, ü)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Eszett (ß)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "German Consonant Clusters", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Word Stress Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "German Ch Sounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Long and Short Vowels", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Final Devoicing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronunciation and Phonetics"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Vocabulary",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Numbers and Mathematics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Time and Calendar", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Family and Relationships", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Body and Health", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Food and Drinks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Clothing and Appearance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "House and Home", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Nature and Environment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Work and Professions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Education and School", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Transportation and Travel", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Sports and Hobbies", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Weather and Seasons", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Emotions and Personality", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Technology and Science", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Shopping and Services", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "City and Directions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Politics and Society", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Arts and Culture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" },
//                         { name: "Compound Words", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Vocabulary"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Grammar - Nouns and Articles",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Definite Articles (der, die, das)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Indefinite Articles (ein, eine)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Gender Rules and Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Plural Formation Rules", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Weak Nouns (N-Declension)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Compound Noun Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Grammar - Nouns and Articles"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Cases",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Nominative Case", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Cases"], learning_area: "Humanities" },
//                         { name: "Accusative Case", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Cases"], learning_area: "Humanities" },
//                         { name: "Dative Case", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Cases"], learning_area: "Humanities" },
//                         { name: "Genitive Case", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Cases"], learning_area: "Humanities" },
//                         { name: "Case with Prepositions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Cases"], learning_area: "Humanities" },
//                         { name: "Two-Way Prepositions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Cases"], learning_area: "Humanities" },
//                         { name: "Case in Time Expressions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Cases"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Verbs - Present Tense",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Regular Verb Conjugation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Sein (to be)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Haben (to have)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Werden (to become)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Strong Verb Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Modal Verbs (können, müssen, wollen)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Separable Prefix Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Inseparable Prefix Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Reflexive Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Imperative Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Present Tense"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Verbs - Past Tenses",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Perfekt with Haben", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Perfekt with Sein", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Past Participle Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Präteritum (Simple Past)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Plusquamperfekt", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Strong Verb Patterns in Past", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Mixed Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Past Tenses"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Verbs - Future and Conditional",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Futur I (Simple Future)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Futur II (Future Perfect)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Konjunktiv II (Conditional)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Würde + Infinitive", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Conditional Sentences", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Verbs - Future and Conditional"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Subjunctive",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Konjunktiv I (Indirect Speech)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Subjunctive"], learning_area: "Humanities" },
//                         { name: "Konjunktiv II (Hypothetical)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Subjunctive"], learning_area: "Humanities" },
//                         { name: "Subjunctive in Wishes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Subjunctive"], learning_area: "Humanities" },
//                         { name: "Subjunctive in Polite Requests", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Subjunctive"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Word Order",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Basic Word Order (V2 Rule)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Word Order"], learning_area: "Humanities" },
//                         { name: "Inverted Word Order", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Word Order"], learning_area: "Humanities" },
//                         { name: "Subordinate Clause Word Order", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Word Order"], learning_area: "Humanities" },
//                         { name: "Time-Manner-Place", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Word Order"], learning_area: "Humanities" },
//                         { name: "Position of Objects", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Word Order"], learning_area: "Humanities" },
//                         { name: "Verb Bracket Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Word Order"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Pronouns",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Personal Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronouns"], learning_area: "Humanities" },
//                         { name: "Possessive Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronouns"], learning_area: "Humanities" },
//                         { name: "Reflexive Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronouns"], learning_area: "Humanities" },
//                         { name: "Relative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronouns"], learning_area: "Humanities" },
//                         { name: "Demonstrative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronouns"], learning_area: "Humanities" },
//                         { name: "Interrogative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronouns"], learning_area: "Humanities" },
//                         { name: "Indefinite Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Pronouns"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Adjectives and Adverbs",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Adjective Endings (Strong)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adjective Endings (Weak)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adjective Endings (Mixed)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Comparative Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Superlative Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adverb Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Adjectives and Adverbs"], learning_area: "Humanities" },
//                         { name: "Adverb Placement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Adjectives and Adverbs"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "German Culture and Communication",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Formal vs Informal Address (Sie/du)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" },
//                         { name: "German Idioms and Sayings", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Business German", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Regional Dialects Overview", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" },
//                         { name: "German-Speaking Countries", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" },
//                         { name: "German Literature Overview", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" },
//                         { name: "German Media and Culture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Writing Formal Letters", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "German", "German Culture and Communication"], learning_area: "Humanities" }
//                       ]
//                     }
//                   ]
//                 },
//                 { 
//                   name: "Italian", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     {
//                       name: "Italian Pronunciation and Phonetics",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Italian Alphabet and Sounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Double Consonants (Gemination)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Open and Closed Vowels", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "C and G Sounds (Hard and Soft)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Gli and Gn Sounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Stress and Accent Marks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Italian R Sound", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" },
//                         { name: "Regional Pronunciation Variations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronunciation and Phonetics"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Vocabulary",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Numbers and Counting", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Time and Calendar", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Family and Relationships", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Body and Health", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Food and Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Clothing and Fashion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "House and Furniture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Nature and Environment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Work and Professions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Education and School", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Transportation and Travel", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Sports and Hobbies", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Weather and Seasons", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Emotions and Feelings", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Technology and Modern Life", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Shopping and Services", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "City and Directions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Art and Culture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "Music and Opera Terms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" },
//                         { name: "False Friends with English", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Vocabulary"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Grammar - Nouns and Articles",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Definite Articles (il, lo, la, i, gli, le)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Indefinite Articles (un, uno, una)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Gender of Nouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Plural Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Articulated Prepositions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Grammar - Nouns and Articles"], learning_area: "Humanities" },
//                         { name: "Partitive Articles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Grammar - Nouns and Articles"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Verbs - Present Tense",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Regular -ARE Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Regular -ERE Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Regular -IRE Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Essere (to be)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Avere (to have)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Fare (to do/make)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Andare (to go)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Modal Verbs (potere, volere, dovere)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Reflexive Verbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" },
//                         { name: "Present Progressive (stare + gerund)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Present Tense"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Verbs - Past Tenses",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Passato Prossimo with Avere", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Passato Prossimo with Essere", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Past Participle Agreement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Imperfetto Formation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Passato Prossimo vs Imperfetto", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Trapassato Prossimo", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Passato Remoto", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" },
//                         { name: "Trapassato Remoto", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Past Tenses"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Verbs - Future and Conditional",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Futuro Semplice", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Futuro Anteriore", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Condizionale Presente", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Condizionale Passato", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "Future of Probability", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Future and Conditional"], learning_area: "Humanities" },
//                         { name: "If Clauses (Periodo Ipotetico)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Verbs - Future and Conditional"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Subjunctive Mood",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Congiuntivo Presente", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Congiuntivo Passato", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Congiuntivo Imperfetto", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Congiuntivo Trapassato", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive Triggers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Subjunctive Mood"], learning_area: "Humanities" },
//                         { name: "Subjunctive vs Indicative", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Subjunctive Mood"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Pronouns",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Subject Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" },
//                         { name: "Direct Object Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" },
//                         { name: "Indirect Object Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" },
//                         { name: "Combined Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" },
//                         { name: "Ci and Ne", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" },
//                         { name: "Relative Pronouns (che, cui, quale)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" },
//                         { name: "Possessive Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" },
//                         { name: "Demonstrative Pronouns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Pronouns"], learning_area: "Humanities" }
//                       ]
//                     },
//                     {
//                       name: "Italian Culture and Communication",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian"],
//                       learning_area: "Humanities",
//                       children: [
//                         { name: "Formal vs Informal Address (Lei/tu)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Italian Gestures", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Italian Idioms and Proverbs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Regional Dialects", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Italian Cuisine Terms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Italian Art and Architecture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Italian Literature Overview", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" },
//                         { name: "Business Italian", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Italian", "Italian Culture and Communication"], learning_area: "Humanities" }
//                       ]
//                     }
//                   ]
//                 },
//                 { 
//                   name: "Japanese", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Hiragana", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Japanese"], learning_area: "Humanities" },
//                     { name: "Katakana", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Japanese"], learning_area: "Humanities" },
//                     { name: "Kanji - Basic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Japanese"], learning_area: "Humanities" },
//                     { name: "Japanese Particles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Japanese"], learning_area: "Humanities" },
//                     { name: "Japanese Verb Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Japanese"], learning_area: "Humanities" },
//                     { name: "Keigo (Polite Language)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Japanese"], learning_area: "Humanities" },
//                     { name: "Japanese Counters", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Japanese"], learning_area: "Humanities" }
//                   ]
//                 },
//                 { 
//                   name: "Arabic", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Arabic Alphabet", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Arabic"], learning_area: "Humanities" },
//                     { name: "Arabic Script Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Arabic"], learning_area: "Humanities" },
//                     { name: "Arabic Root System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Arabic"], learning_area: "Humanities" },
//                     { name: "Arabic Verb Forms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Arabic"], learning_area: "Humanities" },
//                     { name: "Modern Standard Arabic", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Arabic"], learning_area: "Humanities" },
//                     { name: "Arabic Dialects", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Arabic"], learning_area: "Humanities" }
//                   ]
//                 },
//                 { 
//                   name: "Russian", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Cyrillic Alphabet", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Russian"], learning_area: "Humanities" },
//                     { name: "Russian Cases", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Russian"], learning_area: "Humanities" },
//                     { name: "Russian Verb Aspects", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Russian"], learning_area: "Humanities" },
//                     { name: "Russian Verb of Motion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Russian"], learning_area: "Humanities" },
//                     { name: "Russian Pronunciation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Russian"], learning_area: "Humanities" },
//                     { name: "Russian Vocabulary", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Russian"], learning_area: "Humanities" }
//                   ]
//                 },
//                 { 
//                   name: "Korean", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Hangul (Korean Alphabet)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Korean"], learning_area: "Humanities" },
//                     { name: "Korean Particles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Korean"], learning_area: "Humanities" },
//                     { name: "Korean Honorifics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Korean"], learning_area: "Humanities" },
//                     { name: "Korean Verb Conjugation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Korean"], learning_area: "Humanities" },
//                     { name: "Korean Numbers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Korean"], learning_area: "Humanities" },
//                     { name: "Korean Grammar Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Korean"], learning_area: "Humanities" }
//                   ]
//                 },
//                 { 
//                   name: "Portuguese", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Portuguese Pronunciation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Portuguese"], learning_area: "Humanities" },
//                     { name: "Portuguese Verb Conjugation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Portuguese"], learning_area: "Humanities" },
//                     { name: "Portuguese Subjunctive", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Portuguese"], learning_area: "Humanities" },
//                     { name: "Brazilian vs European Portuguese", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Portuguese"], learning_area: "Humanities" },
//                     { name: "Portuguese Prepositions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Portuguese"], learning_area: "Humanities" },
//                     { name: "Portuguese False Friends", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Portuguese"], learning_area: "Humanities" }
//                   ]
//                 },
//                 { 
//                   name: "Latin", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], 
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Latin Declensions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Latin"], learning_area: "Humanities" },
//                     { name: "Latin Verb Conjugations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Latin"], learning_area: "Humanities" },
//                     { name: "Latin Cases", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Latin"], learning_area: "Humanities" },
//                     { name: "Latin Vocabulary", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Latin"], learning_area: "Humanities" },
//                     { name: "Classical Latin Texts", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages", "Latin"], learning_area: "Humanities" }
//                   ]
//                 },
//                 { name: "Ancient Greek", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Languages"], learning_area: "Humanities" }
//               ]
//             },
//             {
//               name: "Geography",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Humanities"],
//               learning_area: "Humanities",
//               children: [
//                 {
//                   name: "Physical Geography",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Landforms and Topography", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Physical Geography"], learning_area: "Humanities" },
//                     { name: "Climate Zones", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Physical Geography"], learning_area: "Humanities" },
//                     { name: "Water Cycle", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Physical Geography"], learning_area: "Humanities" },
//                     { name: "Plate Tectonics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Physical Geography"], learning_area: "Humanities" },
//                     { name: "Erosion and Weathering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Physical Geography"], learning_area: "Humanities" },
//                     { name: "Biomes and Ecosystems", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Physical Geography"], learning_area: "Humanities" },
//                     { name: "Natural Resources", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Physical Geography"], learning_area: "Humanities" }
//                   ]
//                 },
//                 {
//                   name: "Human Geography",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Population Distribution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Human Geography"], learning_area: "Humanities" },
//                     { name: "Urban Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Human Geography"], learning_area: "Humanities" },
//                     { name: "Cultural Geography", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Human Geography"], learning_area: "Humanities" },
//                     { name: "Economic Geography", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Human Geography"], learning_area: "Humanities" },
//                     { name: "Political Geography", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Human Geography"], learning_area: "Humanities" },
//                     { name: "Migration Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Human Geography"], learning_area: "Humanities" },
//                     { name: "Globalization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Human Geography"], learning_area: "Humanities" }
//                   ]
//                 },
//                 {
//                   name: "World Regions",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "North America", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "World Regions"], learning_area: "Humanities" },
//                     { name: "South America", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "World Regions"], learning_area: "Humanities" },
//                     { name: "Europe", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "World Regions"], learning_area: "Humanities" },
//                     { name: "Africa", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "World Regions"], learning_area: "Humanities" },
//                     { name: "Asia", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "World Regions"], learning_area: "Humanities" },
//                     { name: "Oceania", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "World Regions"], learning_area: "Humanities" },
//                     { name: "Antarctica", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "World Regions"], learning_area: "Humanities" }
//                   ]
//                 },
//                 {
//                   name: "Cartography",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography"],
//                   learning_area: "Humanities",
//                   children: [
//                     { name: "Map Reading", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Cartography"], learning_area: "Humanities" },
//                     { name: "Latitude and Longitude", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Cartography"], learning_area: "Humanities" },
//                     { name: "Map Projections", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Cartography"], learning_area: "Humanities" },
//                     { name: "Scale and Distance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Cartography"], learning_area: "Humanities" },
//                     { name: "GIS Technology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Cartography"], learning_area: "Humanities" },
//                     { name: "Remote Sensing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Geography", "Cartography"], learning_area: "Humanities" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Law",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Humanities"],
//               learning_area: "Humanities",
//               children: [
//                 { name: "Constitutional Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" },
//                 { name: "Criminal Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" },
//                 { name: "Civil Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" },
//                 { name: "International Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" },
//                 { name: "Legal Philosophy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" },
//                 { name: "Legal History", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" },
//                 { name: "Human Rights Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" },
//                 { name: "Comparative Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Humanities", "Law"], learning_area: "Humanities" }
//               ]
//             }
//           ]
//         },
//         {
//           name: "Social Sciences",
//           type: "category",
//           path: ["Knowledge", "Academic Disciplines"],
//           learning_area: "Social Sciences",
//           children: [
//             {
//               name: "Psychology",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Social Sciences"],
//               learning_area: "Social Sciences",
//               children: [
//                 { 
//                   name: "Cognitive Psychology", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology"], 
//                   learning_area: "Social Sciences",
//                   children: [
//                     { name: "Perception", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Cognitive Psychology"], learning_area: "Social Sciences" },
//                     { name: "Attention", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Cognitive Psychology"], learning_area: "Social Sciences" },
//                     { name: "Memory Types", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Cognitive Psychology"], learning_area: "Social Sciences" },
//                     { name: "Language Processing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Cognitive Psychology"], learning_area: "Social Sciences" },
//                     { name: "Problem Solving", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Cognitive Psychology"], learning_area: "Social Sciences" },
//                     { name: "Decision Making", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Cognitive Psychology"], learning_area: "Social Sciences" },
//                     { name: "Cognitive Biases", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Cognitive Psychology"], learning_area: "Social Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Developmental Psychology", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology"], 
//                   learning_area: "Social Sciences",
//                   children: [
//                     { name: "Piaget's Stages", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Developmental Psychology"], learning_area: "Social Sciences" },
//                     { name: "Attachment Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Developmental Psychology"], learning_area: "Social Sciences" },
//                     { name: "Language Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Developmental Psychology"], learning_area: "Social Sciences" },
//                     { name: "Moral Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Developmental Psychology"], learning_area: "Social Sciences" },
//                     { name: "Adolescent Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Developmental Psychology"], learning_area: "Social Sciences" },
//                     { name: "Aging and Cognition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Developmental Psychology"], learning_area: "Social Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Social Psychology", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology"], 
//                   learning_area: "Social Sciences",
//                   children: [
//                     { name: "Social Influence", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Social Psychology"], learning_area: "Social Sciences" },
//                     { name: "Conformity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Social Psychology"], learning_area: "Social Sciences" },
//                     { name: "Group Dynamics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Social Psychology"], learning_area: "Social Sciences" },
//                     { name: "Prejudice and Stereotypes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Social Psychology"], learning_area: "Social Sciences" },
//                     { name: "Attribution Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Social Psychology"], learning_area: "Social Sciences" },
//                     { name: "Attitudes and Persuasion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Social Psychology"], learning_area: "Social Sciences" }
//                   ]
//                 },
//                 { name: "Clinical Psychology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology"], learning_area: "Social Sciences" },
//                 { 
//                   name: "Neuroscience", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology"], 
//                   learning_area: "Social Sciences",
//                   children: [
//                     { name: "Brain Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Neuroscience"], learning_area: "Social Sciences" },
//                     { name: "Neurotransmitters", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Neuroscience"], learning_area: "Social Sciences" },
//                     { name: "Neural Pathways", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Neuroscience"], learning_area: "Social Sciences" },
//                     { name: "Brain Plasticity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Neuroscience"], learning_area: "Social Sciences" },
//                     { name: "Sleep and Consciousness", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Psychology", "Neuroscience"], learning_area: "Social Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Sociology",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Social Sciences"],
//               learning_area: "Social Sciences",
//               children: [
//                 { name: "Social Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Sociology"], learning_area: "Social Sciences" },
//                 { name: "Urban Sociology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Sociology"], learning_area: "Social Sciences" },
//                 { name: "Criminology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Sociology"], learning_area: "Social Sciences" },
//                 { name: "Demography", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Sociology"], learning_area: "Social Sciences" }
//               ]
//             },
//             {
//               name: "Economics",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Social Sciences"],
//               learning_area: "Social Sciences",
//               children: [
//                 { 
//                   name: "Microeconomics", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics"], 
//                   learning_area: "Social Sciences",
//                   children: [
//                     { name: "Supply and Demand", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Elasticity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Consumer Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Production Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Market Structures", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Perfect Competition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Monopoly", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Oligopoly", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Game Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" },
//                     { name: "Market Failure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Microeconomics"], learning_area: "Social Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Macroeconomics", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics"], 
//                   learning_area: "Social Sciences",
//                   children: [
//                     { name: "GDP and National Income", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Inflation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Unemployment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Business Cycles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Fiscal Policy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Monetary Policy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Central Banking", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Exchange Rates", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" },
//                     { name: "Economic Growth", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics", "Macroeconomics"], learning_area: "Social Sciences" }
//                   ]
//                 },
//                 { name: "International Economics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics"], learning_area: "Social Sciences" },
//                 { name: "Behavioral Economics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Economics"], learning_area: "Social Sciences" }
//               ]
//             },
//             {
//               name: "Linguistics",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Social Sciences"],
//               learning_area: "Social Sciences",
//               children: [
//                 { name: "Phonetics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Linguistics"], learning_area: "Social Sciences" },
//                 { name: "Syntax", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Linguistics"], learning_area: "Social Sciences" },
//                 { name: "Semantics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Linguistics"], learning_area: "Social Sciences" },
//                 { name: "Sociolinguistics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Linguistics"], learning_area: "Social Sciences" },
//                 { name: "Historical Linguistics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Linguistics"], learning_area: "Social Sciences" },
//                 { name: "Psycholinguistics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Linguistics"], learning_area: "Social Sciences" }
//               ]
//             },
//             {
//               name: "Political Science",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Social Sciences"],
//               learning_area: "Social Sciences",
//               children: [
//                 { name: "Comparative Politics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Political Science"], learning_area: "Social Sciences" },
//                 { name: "International Relations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Political Science"], learning_area: "Social Sciences" },
//                 { name: "Political Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Political Science"], learning_area: "Social Sciences" },
//                 { name: "Public Policy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Political Science"], learning_area: "Social Sciences" },
//                 { name: "Constitutional Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Political Science"], learning_area: "Social Sciences" },
//                 { name: "Electoral Systems", type: "skill", path: ["Knowledge", "Academic Disciplines", "Social Sciences", "Political Science"], learning_area: "Social Sciences" }
//               ]
//             }
//           ]
//         },
//         {
//           name: "Natural Sciences",
//           type: "category",
//           path: ["Knowledge", "Academic Disciplines"],
//           learning_area: "Natural Sciences",
//           children: [
//             {
//               name: "Physics",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Natural Sciences"],
//               learning_area: "Natural Sciences",
//               children: [
//                 { 
//                   name: "Classical Mechanics", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Kinematics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" },
//                     { name: "Newton's Laws of Motion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" },
//                     { name: "Work and Energy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" },
//                     { name: "Momentum and Collisions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" },
//                     { name: "Rotational Motion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" },
//                     { name: "Gravitation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" },
//                     { name: "Simple Harmonic Motion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" },
//                     { name: "Waves and Sound", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Classical Mechanics"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { name: "Quantum Mechanics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics"], learning_area: "Natural Sciences" },
//                 { 
//                   name: "Thermodynamics", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Temperature and Heat", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Thermodynamics"], learning_area: "Natural Sciences" },
//                     { name: "First Law of Thermodynamics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Thermodynamics"], learning_area: "Natural Sciences" },
//                     { name: "Second Law of Thermodynamics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Thermodynamics"], learning_area: "Natural Sciences" },
//                     { name: "Entropy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Thermodynamics"], learning_area: "Natural Sciences" },
//                     { name: "Heat Engines", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Thermodynamics"], learning_area: "Natural Sciences" },
//                     { name: "Phase Transitions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Thermodynamics"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Electromagnetism", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Electric Charge and Coulomb's Law", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "Electric Fields", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "Electric Potential", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "Capacitance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "Electric Current and Resistance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "DC Circuits", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "Magnetic Fields", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "Electromagnetic Induction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "AC Circuits", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" },
//                     { name: "Electromagnetic Waves", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Electromagnetism"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Physics Laboratory Skills",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Using Vernier Calipers and Micrometers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Oscilloscope Operation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Multimeter Usage", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Force Sensor Calibration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Motion Tracking and Video Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Error Analysis and Uncertainty", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Data Logger Setup", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Spectroscopy Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Laboratory Skills"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Physics Experiments",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Pendulum Period Experiment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Projectile Motion Lab", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Hooke's Law and Spring Constants", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Conservation of Momentum with Collisions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Specific Heat Capacity Determination", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Ohm's Law Verification", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "RC Circuit Time Constants", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Magnetic Field Mapping", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Diffraction and Interference Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Photoelectric Effect Demonstration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Standing Wave Patterns", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Moment of Inertia Measurement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Physics", "Physics Experiments"], learning_area: "Natural Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Chemistry",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Natural Sciences"],
//               learning_area: "Natural Sciences",
//               children: [
//                 { 
//                   name: "General Chemistry",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Atomic Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Electron Configuration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Periodic Table Trends", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Chemical Bonding", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Molecular Geometry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Stoichiometry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Gas Laws", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Solutions and Solubility", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Acids and Bases", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Oxidation-Reduction Reactions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Chemical Equilibrium", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Thermochemistry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "General Chemistry"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Organic Chemistry", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Alkanes and Cycloalkanes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Alkenes and Alkynes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Aromatic Compounds", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Alcohols and Ethers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Aldehydes and Ketones", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Carboxylic Acids", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Amines and Amides", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Stereochemistry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" },
//                     { name: "Reaction Mechanisms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Organic Chemistry"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { name: "Inorganic Chemistry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry"], learning_area: "Natural Sciences" },
//                 { name: "Physical Chemistry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry"], learning_area: "Natural Sciences" },
//                 { 
//                   name: "Biochemistry", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Amino Acids and Proteins", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Biochemistry"], learning_area: "Natural Sciences" },
//                     { name: "Carbohydrates", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Biochemistry"], learning_area: "Natural Sciences" },
//                     { name: "Lipids and Membranes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Biochemistry"], learning_area: "Natural Sciences" },
//                     { name: "Nucleic Acids", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Biochemistry"], learning_area: "Natural Sciences" },
//                     { name: "Enzymes and Catalysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Biochemistry"], learning_area: "Natural Sciences" },
//                     { name: "Metabolism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Biochemistry"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Chemistry Laboratory Skills",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Laboratory Safety and PPE", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Using Analytical Balances", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Pipetting and Volumetric Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Bunsen Burner Operation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Filtration Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Crystallization and Recrystallization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Distillation Setup", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Chromatography Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "pH Meter Calibration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Spectrophotometer Use", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Titration Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Chemical Waste Disposal", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Laboratory Skills"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Chemistry Experiments",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Flame Test for Metal Ions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Synthesis of Aspirin", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Acid-Base Titration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Redox Titration with Permanganate", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Determination of Avogadro's Number", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Hess's Law and Calorimetry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Electrochemical Cell Construction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Rate of Reaction Studies", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Equilibrium Constant Determination", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Qualitative Analysis of Cations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Synthesis of Nylon", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Beer's Law and Concentration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Crystal Growing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Soap Making Saponification", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Chemistry", "Chemistry Experiments"], learning_area: "Natural Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Biology",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Natural Sciences"],
//               learning_area: "Natural Sciences",
//               children: [
//                 { 
//                   name: "Cell Biology", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Cell Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Prokaryotic vs Eukaryotic Cells", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Cell Membrane Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Organelles and Functions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Cell Transport Mechanisms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Cellular Respiration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Photosynthesis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Cell Division - Mitosis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Cell Division - Meiosis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" },
//                     { name: "Cell Signaling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Cell Biology"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Genetics", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "DNA Structure and Replication", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "RNA and Transcription", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Protein Synthesis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Mendelian Genetics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Punnett Squares", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Non-Mendelian Inheritance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Chromosomes and Karyotypes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Genetic Mutations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Gene Expression Regulation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" },
//                     { name: "Genetic Engineering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Genetics"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Evolution", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Natural Selection", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Darwin's Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Evidence for Evolution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Fossil Record", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Comparative Anatomy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Molecular Evolution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Speciation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Hardy-Weinberg Equilibrium", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Genetic Drift", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" },
//                     { name: "Adaptive Radiation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Evolution"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Ecology", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Ecosystem Components", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Food Chains and Webs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Energy Pyramids", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Nutrient Cycles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Population Dynamics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Community Interactions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Succession", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Biomes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Conservation Biology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" },
//                     { name: "Climate Change Impact", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Ecology"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Human Biology", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology"], 
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Digestive System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Respiratory System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Circulatory System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Nervous System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Endocrine System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Immune System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Reproductive System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Skeletal System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" },
//                     { name: "Muscular System", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Human Biology"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Biology Laboratory Skills",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Microscope Operation and Maintenance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Slide Preparation and Staining", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Aseptic Technique", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Cell Culture Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Gel Electrophoresis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "PCR Technique", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Dissection Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Centrifuge Operation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Incubator and Autoclave Use", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Field Sampling Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Biological Drawing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" },
//                     { name: "Data Collection and Recording", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Laboratory Skills"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Biology Experiments",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Observing Cell Division", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Osmosis in Plant Cells", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Enzyme Activity Investigation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Photosynthesis Rate Measurement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Respiration Rate in Yeast", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "DNA Extraction from Fruit", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Bacterial Gram Staining", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Blood Typing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Heart Rate and Exercise", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Drosophila Genetics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Plant Tropism Studies", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Ecological Quadrat Sampling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Water Quality Testing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Frog Dissection", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" },
//                     { name: "Flower Dissection", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Biology", "Biology Experiments"], learning_area: "Natural Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Earth Sciences",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Natural Sciences"],
//               learning_area: "Natural Sciences",
//               children: [
//                 { name: "Geology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Earth Sciences"], learning_area: "Natural Sciences" },
//                 { name: "Meteorology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Earth Sciences"], learning_area: "Natural Sciences" },
//                 { name: "Oceanography", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Earth Sciences"], learning_area: "Natural Sciences" },
//                 { name: "Climatology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Earth Sciences"], learning_area: "Natural Sciences" },
//                 { name: "Paleontology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Earth Sciences"], learning_area: "Natural Sciences" },
//                 { name: "Seismology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Earth Sciences"], learning_area: "Natural Sciences" }
//               ]
//             },
//             {
//               name: "Astronomy",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Natural Sciences"],
//               learning_area: "Natural Sciences",
//               children: [
//                 { name: "Planetary Science", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Astronomy"], learning_area: "Natural Sciences" },
//                 { name: "Stellar Astronomy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Astronomy"], learning_area: "Natural Sciences" },
//                 { name: "Galactic Astronomy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Astronomy"], learning_area: "Natural Sciences" },
//                 { name: "Cosmology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Astronomy"], learning_area: "Natural Sciences" },
//                 { name: "Astrophysics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Astronomy"], learning_area: "Natural Sciences" },
//                 { name: "Astrobiology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Astronomy"], learning_area: "Natural Sciences" }
//               ]
//             },
//             {
//               name: "Environmental Science",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Natural Sciences"],
//               learning_area: "Natural Sciences",
//               children: [
//                 {
//                   name: "Climate Science",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Greenhouse Effect", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Climate Science"], learning_area: "Natural Sciences" },
//                     { name: "Carbon Cycle", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Climate Science"], learning_area: "Natural Sciences" },
//                     { name: "Global Warming", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Climate Science"], learning_area: "Natural Sciences" },
//                     { name: "Ocean Acidification", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Climate Science"], learning_area: "Natural Sciences" },
//                     { name: "Climate Models", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Climate Science"], learning_area: "Natural Sciences" },
//                     { name: "Renewable Energy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Climate Science"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Conservation",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Biodiversity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Conservation"], learning_area: "Natural Sciences" },
//                     { name: "Endangered Species", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Conservation"], learning_area: "Natural Sciences" },
//                     { name: "Habitat Protection", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Conservation"], learning_area: "Natural Sciences" },
//                     { name: "Wildlife Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Conservation"], learning_area: "Natural Sciences" },
//                     { name: "Marine Conservation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Conservation"], learning_area: "Natural Sciences" },
//                     { name: "Forest Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Conservation"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Pollution",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Air Pollution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Pollution"], learning_area: "Natural Sciences" },
//                     { name: "Water Pollution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Pollution"], learning_area: "Natural Sciences" },
//                     { name: "Soil Contamination", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Pollution"], learning_area: "Natural Sciences" },
//                     { name: "Plastic Pollution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Pollution"], learning_area: "Natural Sciences" },
//                     { name: "Noise Pollution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Pollution"], learning_area: "Natural Sciences" },
//                     { name: "Waste Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Pollution"], learning_area: "Natural Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Sustainability",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science"],
//                   learning_area: "Natural Sciences",
//                   children: [
//                     { name: "Sustainable Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Sustainability"], learning_area: "Natural Sciences" },
//                     { name: "Green Technology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Sustainability"], learning_area: "Natural Sciences" },
//                     { name: "Circular Economy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Sustainability"], learning_area: "Natural Sciences" },
//                     { name: "Sustainable Agriculture", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Sustainability"], learning_area: "Natural Sciences" },
//                     { name: "Water Conservation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Sustainability"], learning_area: "Natural Sciences" },
//                     { name: "Energy Efficiency", type: "skill", path: ["Knowledge", "Academic Disciplines", "Natural Sciences", "Environmental Science", "Sustainability"], learning_area: "Natural Sciences" }
//                   ]
//                 }
//               ]
//             }
//           ]
//         },
//         {
//           name: "Formal Sciences",
//           type: "category",
//           path: ["Knowledge", "Academic Disciplines"],
//           learning_area: "Formal Sciences",
//           children: [
//             {
//               name: "Mathematics",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Formal Sciences"],
//               learning_area: "Formal Sciences",
//               children: [
//                 {
//                   name: "Early Math Concepts",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Counting 1-10", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" },
//                     { name: "Counting 1-100", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" },
//                     { name: "Number Recognition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" },
//                     { name: "Shapes Recognition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" },
//                     { name: "Patterns and Sequences", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" },
//                     { name: "Basic Measurements", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" },
//                     { name: "Time Telling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" },
//                     { name: "Money Counting", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Early Math Concepts"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Arithmetic Foundations",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { 
//                       name: "Addition",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"],
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Single Digit Addition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Addition"], learning_area: "Formal Sciences" },
//                         { name: "Double Digit Addition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Addition"], learning_area: "Formal Sciences" },
//                         { name: "Addition with Regrouping", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Addition"], learning_area: "Formal Sciences" },
//                         { name: "Mental Math Addition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Addition"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { 
//                       name: "Subtraction",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"],
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Single Digit Subtraction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Subtraction"], learning_area: "Formal Sciences" },
//                         { name: "Double Digit Subtraction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Subtraction"], learning_area: "Formal Sciences" },
//                         { name: "Subtraction with Borrowing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Subtraction"], learning_area: "Formal Sciences" },
//                         { name: "Mental Math Subtraction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Subtraction"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { 
//                       name: "Multiplication",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"],
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Multiplication Tables 1-5", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Multiplication"], learning_area: "Formal Sciences" },
//                         { name: "Multiplication Tables 6-10", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Multiplication"], learning_area: "Formal Sciences" },
//                         { name: "Multiplication Tables 11-12", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Multiplication"], learning_area: "Formal Sciences" },
//                         { name: "Multi-Digit Multiplication", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Multiplication"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { 
//                       name: "Division",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"],
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Division Facts", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Division"], learning_area: "Formal Sciences" },
//                         { name: "Long Division", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Division"], learning_area: "Formal Sciences" },
//                         { name: "Division with Remainders", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Division"], learning_area: "Formal Sciences" },
//                         { name: "Divisibility Rules", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Division"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { name: "Order of Operations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"], learning_area: "Formal Sciences" },
//                     { 
//                       name: "Fractions",
//                       type: "category",
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"],
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Understanding Fractions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Fractions"], learning_area: "Formal Sciences" },
//                         { name: "Equivalent Fractions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Fractions"], learning_area: "Formal Sciences" },
//                         { name: "Adding Fractions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Fractions"], learning_area: "Formal Sciences" },
//                         { name: "Subtracting Fractions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Fractions"], learning_area: "Formal Sciences" },
//                         { name: "Multiplying Fractions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Fractions"], learning_area: "Formal Sciences" },
//                         { name: "Dividing Fractions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Fractions"], learning_area: "Formal Sciences" },
//                         { name: "Mixed Numbers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations", "Fractions"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { name: "Decimals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"], learning_area: "Formal Sciences" },
//                     { name: "Percentages", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"], learning_area: "Formal Sciences" },
//                     { name: "Ratios and Proportions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"], learning_area: "Formal Sciences" },
//                     { name: "Prime Numbers", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"], learning_area: "Formal Sciences" },
//                     { name: "Factors and Multiples", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Arithmetic Foundations"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Algebra",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { 
//                       name: "Elementary Algebra", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Variables and Expressions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Solving Linear Equations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Solving Quadratic Equations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Factoring Polynomials", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Systems of Equations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Inequalities", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Exponents and Radicals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Rational Expressions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Elementary Algebra"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { 
//                       name: "Linear Algebra", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Vectors and Vector Spaces", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Linear Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Matrix Operations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Linear Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Determinants", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Linear Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Eigenvalues and Eigenvectors", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Linear Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Linear Transformations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Linear Algebra"], learning_area: "Formal Sciences" },
//                         { name: "Inner Product Spaces", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra", "Linear Algebra"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { name: "Abstract Algebra", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra"], learning_area: "Formal Sciences" },
//                     { name: "Group Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra"], learning_area: "Formal Sciences" },
//                     { name: "Ring Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Algebra"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Geometry",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Euclidean Geometry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Geometry"], learning_area: "Formal Sciences" },
//                     { name: "Analytic Geometry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Geometry"], learning_area: "Formal Sciences" },
//                     { name: "Trigonometry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Geometry"], learning_area: "Formal Sciences" },
//                     { name: "Differential Geometry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Geometry"], learning_area: "Formal Sciences" },
//                     { name: "Topology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Geometry"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Calculus",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { 
//                       name: "Differential Calculus", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Limits and Continuity", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Definition of Derivative", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Power Rule", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Product and Quotient Rules", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Chain Rule", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Implicit Differentiation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Related Rates", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Optimization Problems", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" },
//                         { name: "L'Hôpital's Rule", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Calculus"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { 
//                       name: "Integral Calculus", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Antiderivatives", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Definite Integrals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Fundamental Theorem of Calculus", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "U-Substitution", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Integration by Parts", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Trigonometric Integrals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Partial Fractions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Improper Integrals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" },
//                         { name: "Areas and Volumes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Integral Calculus"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { name: "Multivariable Calculus", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus"], learning_area: "Formal Sciences" },
//                     { name: "Vector Calculus", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus"], learning_area: "Formal Sciences" },
//                     { 
//                       name: "Differential Equations", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "First-Order ODEs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Equations"], learning_area: "Formal Sciences" },
//                         { name: "Second-Order Linear ODEs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Equations"], learning_area: "Formal Sciences" },
//                         { name: "Systems of ODEs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Equations"], learning_area: "Formal Sciences" },
//                         { name: "Laplace Transforms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Equations"], learning_area: "Formal Sciences" },
//                         { name: "Fourier Series", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Calculus", "Differential Equations"], learning_area: "Formal Sciences" }
//                       ]
//                     }
//                   ]
//                 },
//                 {
//                   name: "Statistics and Probability",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { 
//                       name: "Descriptive Statistics", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Mean, Median, Mode", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Range and Quartiles", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Standard Deviation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Variance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Histograms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Box Plots", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Scatter Plots", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Correlation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Descriptive Statistics"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { 
//                       name: "Probability Theory", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Basic Probability Rules", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Probability Theory"], learning_area: "Formal Sciences" },
//                         { name: "Conditional Probability", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Probability Theory"], learning_area: "Formal Sciences" },
//                         { name: "Bayes' Theorem", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Probability Theory"], learning_area: "Formal Sciences" },
//                         { name: "Permutations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Probability Theory"], learning_area: "Formal Sciences" },
//                         { name: "Combinations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Probability Theory"], learning_area: "Formal Sciences" },
//                         { name: "Expected Value", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Probability Theory"], learning_area: "Formal Sciences" },
//                         { name: "Probability Distributions", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Probability Theory"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { 
//                       name: "Inferential Statistics", 
//                       type: "category", 
//                       path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability"], 
//                       learning_area: "Formal Sciences",
//                       children: [
//                         { name: "Hypothesis Testing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Inferential Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Confidence Intervals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Inferential Statistics"], learning_area: "Formal Sciences" },
//                         { name: "T-Tests", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Inferential Statistics"], learning_area: "Formal Sciences" },
//                         { name: "ANOVA", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Inferential Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Chi-Square Tests", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Inferential Statistics"], learning_area: "Formal Sciences" },
//                         { name: "Regression Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Inferential Statistics"], learning_area: "Formal Sciences" },
//                         { name: "P-Values", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability", "Inferential Statistics"], learning_area: "Formal Sciences" }
//                       ]
//                     },
//                     { name: "Bayesian Statistics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability"], learning_area: "Formal Sciences" },
//                     { name: "Statistical Modeling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Statistics and Probability"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Discrete Mathematics",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Combinatorics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Discrete Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Graph Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Discrete Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Number Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Discrete Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Set Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Discrete Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Boolean Algebra", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Discrete Mathematics"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Applied Mathematics",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics"],
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Mathematical Modeling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Applied Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Numerical Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Applied Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Operations Research", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Applied Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Game Theory", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Applied Mathematics"], learning_area: "Formal Sciences" },
//                     { name: "Mathematical Finance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Mathematics", "Applied Mathematics"], learning_area: "Formal Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Computer Science",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Formal Sciences"],
//               learning_area: "Formal Sciences",
//               children: [
//                 { 
//                   name: "Programming Fundamentals", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science"], 
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Variables and Data Types", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" },
//                     { name: "Control Structures", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" },
//                     { name: "Functions and Procedures", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" },
//                     { name: "Arrays and Lists", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" },
//                     { name: "Loops and Iteration", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" },
//                     { name: "Recursion", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" },
//                     { name: "Error Handling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" },
//                     { name: "Input/Output Operations", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Programming Fundamentals"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Object-Oriented Programming", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science"], 
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Classes and Objects", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Object-Oriented Programming"], learning_area: "Formal Sciences" },
//                     { name: "Encapsulation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Object-Oriented Programming"], learning_area: "Formal Sciences" },
//                     { name: "Inheritance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Object-Oriented Programming"], learning_area: "Formal Sciences" },
//                     { name: "Polymorphism", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Object-Oriented Programming"], learning_area: "Formal Sciences" },
//                     { name: "Abstraction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Object-Oriented Programming"], learning_area: "Formal Sciences" },
//                     { name: "Interfaces and Abstract Classes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Object-Oriented Programming"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Data Structures", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science"], 
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Arrays and Dynamic Arrays", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Linked Lists", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Stacks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Queues", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Trees", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Binary Search Trees", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Heaps", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Hash Tables", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" },
//                     { name: "Graphs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Data Structures"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Algorithms", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science"], 
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Big O Notation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" },
//                     { name: "Sorting Algorithms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" },
//                     { name: "Searching Algorithms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" },
//                     { name: "Graph Algorithms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" },
//                     { name: "Dynamic Programming", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" },
//                     { name: "Greedy Algorithms", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" },
//                     { name: "Divide and Conquer", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" },
//                     { name: "Backtracking", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Algorithms"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Databases", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science"], 
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Relational Database Concepts", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Databases"], learning_area: "Formal Sciences" },
//                     { name: "SQL Basics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Databases"], learning_area: "Formal Sciences" },
//                     { name: "Database Normalization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Databases"], learning_area: "Formal Sciences" },
//                     { name: "Indexes and Query Optimization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Databases"], learning_area: "Formal Sciences" },
//                     { name: "Transactions and ACID", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Databases"], learning_area: "Formal Sciences" },
//                     { name: "NoSQL Databases", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Databases"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Web Development", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science"], 
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "HTML Structure", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Web Development"], learning_area: "Formal Sciences" },
//                     { name: "CSS Styling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Web Development"], learning_area: "Formal Sciences" },
//                     { name: "JavaScript Basics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Web Development"], learning_area: "Formal Sciences" },
//                     { name: "DOM Manipulation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Web Development"], learning_area: "Formal Sciences" },
//                     { name: "RESTful APIs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Web Development"], learning_area: "Formal Sciences" },
//                     { name: "Frontend Frameworks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Web Development"], learning_area: "Formal Sciences" },
//                     { name: "Backend Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Web Development"], learning_area: "Formal Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Machine Learning", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science"], 
//                   learning_area: "Formal Sciences",
//                   children: [
//                     { name: "Supervised Learning", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Machine Learning"], learning_area: "Formal Sciences" },
//                     { name: "Unsupervised Learning", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Machine Learning"], learning_area: "Formal Sciences" },
//                     { name: "Neural Networks", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Machine Learning"], learning_area: "Formal Sciences" },
//                     { name: "Deep Learning", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Machine Learning"], learning_area: "Formal Sciences" },
//                     { name: "Natural Language Processing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Machine Learning"], learning_area: "Formal Sciences" },
//                     { name: "Computer Vision", type: "skill", path: ["Knowledge", "Academic Disciplines", "Formal Sciences", "Computer Science", "Machine Learning"], learning_area: "Formal Sciences" }
//                   ]
//                 }
//               ]
//             }
//           ]
//         },
//         {
//           name: "Applied Sciences",
//           type: "category",
//           path: ["Knowledge", "Academic Disciplines"],
//           learning_area: "Applied Sciences",
//           children: [
//             {
//               name: "Engineering",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Applied Sciences"],
//               learning_area: "Applied Sciences",
//               children: [
//                 { 
//                   name: "Civil Engineering", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering"], 
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Structural Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Civil Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Bridge Design", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Civil Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Transportation Engineering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Civil Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Geotechnical Engineering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Civil Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Water Resources", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Civil Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Construction Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Civil Engineering"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Mechanical Engineering", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering"], 
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Statics and Dynamics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Mechanical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Materials Science", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Mechanical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Fluid Mechanics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Mechanical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Heat Transfer", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Mechanical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Machine Design", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Mechanical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Manufacturing Processes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Mechanical Engineering"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Electrical Engineering", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering"], 
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Circuit Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Electrical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Digital Electronics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Electrical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Power Systems", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Electrical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Control Systems", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Electrical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Signal Processing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Electrical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Microprocessors", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Electrical Engineering"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 { name: "Software Engineering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering"], learning_area: "Applied Sciences" },
//                 { 
//                   name: "Robotics", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering"], 
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Robot Kinematics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Robotics"], learning_area: "Applied Sciences" },
//                     { name: "Sensors and Actuators", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Robotics"], learning_area: "Applied Sciences" },
//                     { name: "Computer Vision", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Robotics"], learning_area: "Applied Sciences" },
//                     { name: "Path Planning", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Robotics"], learning_area: "Applied Sciences" },
//                     { name: "Machine Learning for Robotics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Robotics"], learning_area: "Applied Sciences" },
//                     { name: "Human-Robot Interaction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Robotics"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Aerospace Engineering", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering"], 
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Aerodynamics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Aerospace Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Propulsion Systems", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Aerospace Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Aircraft Design", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Aerospace Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Orbital Mechanics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Aerospace Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Spacecraft Systems", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Aerospace Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Flight Dynamics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Aerospace Engineering"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 { 
//                   name: "Biomedical Engineering", 
//                   type: "category", 
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering"], 
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Medical Imaging", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Biomedical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Biomaterials", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Biomedical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Prosthetics Design", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Biomedical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Tissue Engineering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Biomedical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Medical Device Design", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Biomedical Engineering"], learning_area: "Applied Sciences" },
//                     { name: "Biomechanics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Engineering", "Biomedical Engineering"], learning_area: "Applied Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Medicine",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Applied Sciences"],
//               learning_area: "Applied Sciences",
//               children: [
//                 { name: "Anatomy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Medicine"], learning_area: "Applied Sciences" },
//                 { name: "Physiology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Medicine"], learning_area: "Applied Sciences" },
//                 { name: "Pathology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Medicine"], learning_area: "Applied Sciences" },
//                 { name: "Pharmacology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Medicine"], learning_area: "Applied Sciences" }
//               ]
//             },
//             {
//               name: "Business and Economics",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Applied Sciences"],
//               learning_area: "Applied Sciences",
//               children: [
//                 {
//                   name: "Business Fundamentals",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Business Models", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Business Fundamentals"], learning_area: "Applied Sciences" },
//                     { name: "Market Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Business Fundamentals"], learning_area: "Applied Sciences" },
//                     { name: "Competitive Strategy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Business Fundamentals"], learning_area: "Applied Sciences" },
//                     { name: "SWOT Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Business Fundamentals"], learning_area: "Applied Sciences" },
//                     { name: "Business Plan Writing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Business Fundamentals"], learning_area: "Applied Sciences" },
//                     { name: "Value Chain Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Business Fundamentals"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Marketing",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Marketing Mix (4Ps)", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Marketing"], learning_area: "Applied Sciences" },
//                     { name: "Consumer Behavior", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Marketing"], learning_area: "Applied Sciences" },
//                     { name: "Brand Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Marketing"], learning_area: "Applied Sciences" },
//                     { name: "Digital Marketing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Marketing"], learning_area: "Applied Sciences" },
//                     { name: "Market Segmentation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Marketing"], learning_area: "Applied Sciences" },
//                     { name: "Advertising Strategy", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Marketing"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Finance",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Financial Statements", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Finance"], learning_area: "Applied Sciences" },
//                     { name: "Cash Flow Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Finance"], learning_area: "Applied Sciences" },
//                     { name: "Investment Analysis", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Finance"], learning_area: "Applied Sciences" },
//                     { name: "Risk Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Finance"], learning_area: "Applied Sciences" },
//                     { name: "Corporate Finance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Finance"], learning_area: "Applied Sciences" },
//                     { name: "Financial Ratios", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Finance"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Entrepreneurship",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Startup Fundamentals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Entrepreneurship"], learning_area: "Applied Sciences" },
//                     { name: "Venture Capital", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Entrepreneurship"], learning_area: "Applied Sciences" },
//                     { name: "Product Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Entrepreneurship"], learning_area: "Applied Sciences" },
//                     { name: "Scaling Strategies", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Entrepreneurship"], learning_area: "Applied Sciences" },
//                     { name: "Lean Startup Method", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Entrepreneurship"], learning_area: "Applied Sciences" },
//                     { name: "Pitch Deck Creation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Entrepreneurship"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Operations Management",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Supply Chain Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Operations Management"], learning_area: "Applied Sciences" },
//                     { name: "Quality Control", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Operations Management"], learning_area: "Applied Sciences" },
//                     { name: "Inventory Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Operations Management"], learning_area: "Applied Sciences" },
//                     { name: "Process Optimization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Operations Management"], learning_area: "Applied Sciences" },
//                     { name: "Six Sigma", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Operations Management"], learning_area: "Applied Sciences" },
//                     { name: "Lean Manufacturing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Business and Economics", "Operations Management"], learning_area: "Applied Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Health and Physical Education",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Applied Sciences"],
//               learning_area: "Applied Sciences",
//               children: [
//                 {
//                   name: "Physical Fitness",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Cardiovascular Fitness", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Physical Fitness"], learning_area: "Applied Sciences" },
//                     { name: "Strength Training", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Physical Fitness"], learning_area: "Applied Sciences" },
//                     { name: "Flexibility and Stretching", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Physical Fitness"], learning_area: "Applied Sciences" },
//                     { name: "Body Composition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Physical Fitness"], learning_area: "Applied Sciences" },
//                     { name: "Exercise Physiology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Physical Fitness"], learning_area: "Applied Sciences" },
//                     { name: "Fitness Assessment", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Physical Fitness"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Sports Science",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Biomechanics of Movement", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Sports Science"], learning_area: "Applied Sciences" },
//                     { name: "Sports Psychology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Sports Science"], learning_area: "Applied Sciences" },
//                     { name: "Athletic Performance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Sports Science"], learning_area: "Applied Sciences" },
//                     { name: "Sports Nutrition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Sports Science"], learning_area: "Applied Sciences" },
//                     { name: "Injury Prevention", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Sports Science"], learning_area: "Applied Sciences" },
//                     { name: "Recovery Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Sports Science"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Team Sports",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Basketball Fundamentals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Team Sports"], learning_area: "Applied Sciences" },
//                     { name: "Soccer/Football Skills", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Team Sports"], learning_area: "Applied Sciences" },
//                     { name: "Baseball/Softball", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Team Sports"], learning_area: "Applied Sciences" },
//                     { name: "Volleyball Techniques", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Team Sports"], learning_area: "Applied Sciences" },
//                     { name: "American Football", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Team Sports"], learning_area: "Applied Sciences" },
//                     { name: "Team Strategy and Tactics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Team Sports"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Individual Sports",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Swimming Strokes", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Individual Sports"], learning_area: "Applied Sciences" },
//                     { name: "Track and Field Events", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Individual Sports"], learning_area: "Applied Sciences" },
//                     { name: "Tennis Fundamentals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Individual Sports"], learning_area: "Applied Sciences" },
//                     { name: "Golf Basics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Individual Sports"], learning_area: "Applied Sciences" },
//                     { name: "Martial Arts", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Individual Sports"], learning_area: "Applied Sciences" },
//                     { name: "Gymnastics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Individual Sports"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Health Education",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Personal Hygiene", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Health Education"], learning_area: "Applied Sciences" },
//                     { name: "Disease Prevention", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Health Education"], learning_area: "Applied Sciences" },
//                     { name: "First Aid and CPR", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Health Education"], learning_area: "Applied Sciences" },
//                     { name: "Substance Abuse Prevention", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Health Education"], learning_area: "Applied Sciences" },
//                     { name: "Sexual Health Education", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Health Education"], learning_area: "Applied Sciences" },
//                     { name: "Mental Health Awareness", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Health and Physical Education", "Health Education"], learning_area: "Applied Sciences" }
//                   ]
//                 }
//               ]
//             },
//             {
//               name: "Culinary Arts and Nutrition",
//               type: "category",
//               path: ["Knowledge", "Academic Disciplines", "Applied Sciences"],
//               learning_area: "Applied Sciences",
//               children: [
//                 {
//                   name: "Basic Cooking Techniques",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Knife Skills and Safety", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Boiling and Simmering", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Sautéing and Stir-Frying", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Roasting and Baking", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Grilling and Broiling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Steaming and Poaching", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Braising and Stewing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Deep Frying", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" },
//                     { name: "Food Safety and Hygiene", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Basic Cooking Techniques"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Baking and Pastry",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Bread Making", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Yeast and Fermentation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Cake Baking", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Cookie and Biscuit Making", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Pie and Tart Making", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Pastry Doughs", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Frosting and Decorating", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Chocolate Work", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" },
//                     { name: "Sugar Art", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Baking and Pastry"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "World Cuisines",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Italian Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "French Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "Chinese Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "Japanese Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "Indian Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "Mexican Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "Mediterranean Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "Thai Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "Middle Eastern Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" },
//                     { name: "African Cuisine", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "World Cuisines"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Nutrition Science",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Macronutrients", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Micronutrients", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Vitamins and Minerals", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Caloric Balance", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Dietary Guidelines", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Food Labels Reading", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Meal Planning", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Special Diets", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Sports Nutrition", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" },
//                     { name: "Food Allergies and Intolerances", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Nutrition Science"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Food Science",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Food Chemistry", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" },
//                     { name: "Maillard Reaction", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" },
//                     { name: "Emulsification", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" },
//                     { name: "Gelation and Thickening", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" },
//                     { name: "Fermentation Science", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" },
//                     { name: "Food Preservation Methods", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" },
//                     { name: "Food Microbiology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" },
//                     { name: "Sensory Evaluation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Food Science"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Professional Kitchen Skills",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Menu Development", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" },
//                     { name: "Recipe Scaling", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" },
//                     { name: "Kitchen Organization", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" },
//                     { name: "Cost Control", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" },
//                     { name: "Inventory Management", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" },
//                     { name: "Food Plating and Presentation", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" },
//                     { name: "Catering and Events", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" },
//                     { name: "Restaurant Service", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Professional Kitchen Skills"], learning_area: "Applied Sciences" }
//                   ]
//                 },
//                 {
//                   name: "Beverages",
//                   type: "category",
//                   path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition"],
//                   learning_area: "Applied Sciences",
//                   children: [
//                     { name: "Coffee and Espresso", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Beverages"], learning_area: "Applied Sciences" },
//                     { name: "Tea Varieties and Brewing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Beverages"], learning_area: "Applied Sciences" },
//                     { name: "Wine Basics", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Beverages"], learning_area: "Applied Sciences" },
//                     { name: "Beer and Brewing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Beverages"], learning_area: "Applied Sciences" },
//                     { name: "Cocktails and Mixology", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Beverages"], learning_area: "Applied Sciences" },
//                     { name: "Smoothies and Juices", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Beverages"], learning_area: "Applied Sciences" },
//                     { name: "Food and Beverage Pairing", type: "skill", path: ["Knowledge", "Academic Disciplines", "Applied Sciences", "Culinary Arts and Nutrition", "Beverages"], learning_area: "Applied Sciences" }
//                   ]
//                 }
//               ]
//             }
//           ]
//         }
//       ]
//     },
//     {
//       name: "Applied Knowledge",
//       type: "category",
//       path: ["Knowledge"],
//       learning_area: "Applied Knowledge",
//       children: [
//         {
//           name: "Life Skills",
//           type: "category",
//           path: ["Knowledge", "Applied Knowledge"],
//           learning_area: "Applied Knowledge",
//           children: [
//             { 
//               name: "Financial Literacy", 
//               type: "category", 
//               path: ["Knowledge", "Applied Knowledge", "Life Skills"], 
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Budgeting Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Saving and Investing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Understanding Credit", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Tax Fundamentals", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Insurance Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Retirement Planning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Compound Interest", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Stock Market Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Financial Literacy"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             { 
//               name: "Time Management", 
//               type: "category", 
//               path: ["Knowledge", "Applied Knowledge", "Life Skills"], 
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Goal Setting", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Time Management"], learning_area: "Applied Knowledge" },
//                 { name: "Priority Matrix", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Time Management"], learning_area: "Applied Knowledge" },
//                 { name: "Pomodoro Technique", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Time Management"], learning_area: "Applied Knowledge" },
//                 { name: "Calendar Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Time Management"], learning_area: "Applied Knowledge" },
//                 { name: "Avoiding Procrastination", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Time Management"], learning_area: "Applied Knowledge" },
//                 { name: "Task Batching", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Time Management"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             { 
//               name: "Communication Skills", 
//               type: "category", 
//               path: ["Knowledge", "Applied Knowledge", "Life Skills"], 
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Active Listening", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Communication Skills"], learning_area: "Applied Knowledge" },
//                 { name: "Written Communication", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Communication Skills"], learning_area: "Applied Knowledge" },
//                 { name: "Public Speaking", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Communication Skills"], learning_area: "Applied Knowledge" },
//                 { name: "Nonverbal Communication", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Communication Skills"], learning_area: "Applied Knowledge" },
//                 { name: "Conflict Resolution", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Communication Skills"], learning_area: "Applied Knowledge" },
//                 { name: "Emotional Intelligence", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Communication Skills"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             { 
//               name: "Critical Thinking", 
//               type: "category", 
//               path: ["Knowledge", "Applied Knowledge", "Life Skills"], 
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Logical Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Critical Thinking"], learning_area: "Applied Knowledge" },
//                 { name: "Identifying Logical Fallacies", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Critical Thinking"], learning_area: "Applied Knowledge" },
//                 { name: "Evidence Evaluation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Critical Thinking"], learning_area: "Applied Knowledge" },
//                 { name: "Argument Analysis", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Critical Thinking"], learning_area: "Applied Knowledge" },
//                 { name: "Problem-Solving Methods", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Critical Thinking"], learning_area: "Applied Knowledge" },
//                 { name: "Decision Making Frameworks", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Critical Thinking"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             { 
//               name: "Health and Wellness", 
//               type: "category", 
//               path: ["Knowledge", "Applied Knowledge", "Life Skills"], 
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Nutrition Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Health and Wellness"], learning_area: "Applied Knowledge" },
//                 { name: "Exercise Fundamentals", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Health and Wellness"], learning_area: "Applied Knowledge" },
//                 { name: "Sleep Hygiene", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Health and Wellness"], learning_area: "Applied Knowledge" },
//                 { name: "Stress Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Health and Wellness"], learning_area: "Applied Knowledge" },
//                 { name: "Mental Health Awareness", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Health and Wellness"], learning_area: "Applied Knowledge" },
//                 { name: "Preventive Healthcare", type: "skill", path: ["Knowledge", "Applied Knowledge", "Life Skills", "Health and Wellness"], learning_area: "Applied Knowledge" }
//               ]
//             }
//           ]
//         },
//         {
//           name: "Professional Skills",
//           type: "category",
//           path: ["Knowledge", "Applied Knowledge"],
//           learning_area: "Applied Knowledge",
//           children: [
//             { name: "Leadership", type: "skill", path: ["Knowledge", "Applied Knowledge", "Professional Skills"], learning_area: "Applied Knowledge" },
//             { name: "Project Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Professional Skills"], learning_area: "Applied Knowledge" },
//             { name: "Public Speaking", type: "skill", path: ["Knowledge", "Applied Knowledge", "Professional Skills"], learning_area: "Applied Knowledge" },
//             { name: "Networking", type: "skill", path: ["Knowledge", "Applied Knowledge", "Professional Skills"], learning_area: "Applied Knowledge" }
//           ]
//         },
//         {
//           name: "Creative Skills",
//           type: "category",
//           path: ["Knowledge", "Applied Knowledge"],
//           learning_area: "Applied Knowledge",
//           children: [
//             { name: "Creative Writing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Creative Skills"], learning_area: "Applied Knowledge" },
//             { name: "Design Thinking", type: "skill", path: ["Knowledge", "Applied Knowledge", "Creative Skills"], learning_area: "Applied Knowledge" },
//             { name: "Innovation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Creative Skills"], learning_area: "Applied Knowledge" },
//             { name: "Problem Solving", type: "skill", path: ["Knowledge", "Applied Knowledge", "Creative Skills"], learning_area: "Applied Knowledge" }
//           ]
//         },
//         {
//           name: "Technical Skills",
//           type: "category",
//           path: ["Knowledge", "Applied Knowledge"],
//           learning_area: "Applied Knowledge",
//           children: [
//             {
//               name: "Digital Literacy",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Computer Hardware Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Operating Systems", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "File Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Internet Navigation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Email Communication", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Cloud Storage", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Digital Security Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Password Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Digital Privacy", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" },
//                 { name: "Troubleshooting Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Literacy"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Office Productivity",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Word Processing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Spreadsheet Formulas", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Pivot Tables", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Data Visualization", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Presentation Design", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Database Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Mail Merge", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Macros and Automation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "Collaborative Editing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" },
//                 { name: "PDF Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Office Productivity"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Programming",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Programming Fundamentals", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Variables and Data Types", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Control Structures", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Functions and Methods", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Object-Oriented Programming", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Data Structures", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Algorithms", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Debugging Techniques", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Version Control (Git)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Software Testing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Python Programming", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "JavaScript Programming", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "Java Programming", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "C++ Programming", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" },
//                 { name: "SQL and Databases", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Programming"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Web Development",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "HTML Fundamentals", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "CSS Styling", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "Responsive Design", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "JavaScript DOM Manipulation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "Frontend Frameworks (React, Vue, Angular)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "Backend Development", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "RESTful APIs", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "Web Security", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "Web Accessibility", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "SEO Optimization", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "Web Performance", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" },
//                 { name: "Content Management Systems", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Web Development"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Data Science",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Data Collection Methods", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Data Cleaning and Preprocessing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Exploratory Data Analysis", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Statistical Analysis", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Data Visualization Tools", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Machine Learning Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Supervised Learning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Unsupervised Learning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Deep Learning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Natural Language Processing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Computer Vision", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" },
//                 { name: "Big Data Technologies", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Data Science"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Cybersecurity",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Network Security", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Cryptography Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Malware Analysis", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Penetration Testing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Security Auditing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Incident Response", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Social Engineering", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Firewall Configuration", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "VPN Setup", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" },
//                 { name: "Security Compliance", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cybersecurity"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "AI and Automation",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "AI Fundamentals", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" },
//                 { name: "ChatGPT and LLMs", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" },
//                 { name: "Prompt Engineering", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" },
//                 { name: "AI Image Generation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" },
//                 { name: "Robotic Process Automation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" },
//                 { name: "Workflow Automation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" },
//                 { name: "AI Ethics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" },
//                 { name: "AI in Business", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "AI and Automation"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Mobile Development",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "iOS Development", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" },
//                 { name: "Android Development", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" },
//                 { name: "React Native", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" },
//                 { name: "Flutter Development", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" },
//                 { name: "Mobile UI/UX Design", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" },
//                 { name: "App Store Optimization", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" },
//                 { name: "Push Notifications", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" },
//                 { name: "Mobile Security", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Mobile Development"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Cloud Computing",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Cloud Fundamentals", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Amazon Web Services (AWS)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Microsoft Azure", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Google Cloud Platform", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Containerization (Docker)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Kubernetes", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Serverless Computing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Cloud Security", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "DevOps Practices", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" },
//                 { name: "Infrastructure as Code", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Cloud Computing"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Digital Media",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Photo Editing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Video Editing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Audio Production", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "3D Modeling", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Animation Basics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Graphic Design Software", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Digital Illustration", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Motion Graphics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Streaming and Broadcasting", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" },
//                 { name: "Digital Asset Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Digital Media"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Game Development",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Technical Skills"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Game Design Principles", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" },
//                 { name: "Unity Engine", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" },
//                 { name: "Unreal Engine", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" },
//                 { name: "Game Physics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" },
//                 { name: "Level Design", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" },
//                 { name: "Game AI Programming", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" },
//                 { name: "Multiplayer Networking", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" },
//                 { name: "Game Monetization", type: "skill", path: ["Knowledge", "Applied Knowledge", "Technical Skills", "Game Development"], learning_area: "Applied Knowledge" }
//               ]
//             }
//           ]
//         },
//         {
//           name: "Test Preparation and Assessment",
//           type: "category",
//           path: ["Knowledge", "Applied Knowledge"],
//           learning_area: "Applied Knowledge",
//           children: [
//             {
//               name: "College Entrance Exams",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "SAT Math", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "SAT Reading and Writing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "ACT Math", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "ACT English", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "ACT Reading", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "ACT Science", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "PSAT/NMSQT", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "AP Exam Strategies", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "SAT Subject Tests", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" },
//                 { name: "Essay Writing for Tests", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "College Entrance Exams"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Graduate School Exams",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "GRE Verbal Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "GRE Quantitative Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "GRE Analytical Writing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "GMAT Quantitative", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "GMAT Verbal", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "GMAT Integrated Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "GMAT Analytical Writing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "LSAT Logical Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "LSAT Analytical Reasoning (Logic Games)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "LSAT Reading Comprehension", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "LSAT Writing Sample", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "MCAT Biological Sciences", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "MCAT Physical Sciences", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "MCAT Psychology and Sociology", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" },
//                 { name: "MCAT Critical Analysis", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Graduate School Exams"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "IQ and Cognitive Tests",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Pattern Recognition", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Spatial Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Verbal Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Numerical Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Abstract Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Logical Reasoning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Memory Tests", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Processing Speed", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Raven's Progressive Matrices", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "WAIS Test Components", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Stanford-Binet Test", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Mensa Test Preparation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "IQ and Cognitive Tests"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Language Proficiency Tests",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "TOEFL Reading", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "TOEFL Listening", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "TOEFL Speaking", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "TOEFL Writing", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "IELTS Academic", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "IELTS General Training", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Cambridge English Exams", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "DELE Spanish Proficiency", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "DELF/DALF French", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "HSK Chinese Proficiency", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "JLPT Japanese", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" },
//                 { name: "TestDaF German", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Language Proficiency Tests"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Professional Certification Exams",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "PMP Project Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "CPA Accounting", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "Bar Exam Preparation", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "Medical Board Exams", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "Teaching Certification", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "Real Estate License", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "IT Certifications (CompTIA, Cisco)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "AWS Certification", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "Microsoft Certifications", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" },
//                 { name: "Google Cloud Certification", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Professional Certification Exams"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "K-12 Standardized Tests",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "State Assessment Tests", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Common Core Assessments", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "PARCC Test Prep", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Smarter Balanced Assessment", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "STAAR Test (Texas)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "Regents Exams (New York)", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "ISEE/SSAT Private School", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "CogAT Cognitive Abilities", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "MAP Growth Assessment", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" },
//                 { name: "STAR Assessment", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "K-12 Standardized Tests"], learning_area: "Applied Knowledge" }
//               ]
//             },
//             {
//               name: "Test-Taking Strategies",
//               type: "category",
//               path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment"],
//               learning_area: "Applied Knowledge",
//               children: [
//                 { name: "Time Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Question Analysis", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Elimination Techniques", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Guessing Strategies", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Test Anxiety Management", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Reading Comprehension Tactics", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Math Problem Solving", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Essay Structure and Planning", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Multiple Choice Strategies", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" },
//                 { name: "Computer-Based Test Skills", type: "skill", path: ["Knowledge", "Applied Knowledge", "Test Preparation and Assessment", "Test-Taking Strategies"], learning_area: "Applied Knowledge" }
//               ]
//             }
//           ]
//         }
//       ]
//     }
//   ]
// };