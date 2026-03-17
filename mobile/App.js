/**
 * English File Mobile App
 * Learn English through English - NO RUSSIAN!
 * Based on English File (Oxford) 4th Edition
 */

import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TouchableOpacity, 
  ScrollView,
  FlatList,
  SafeAreaView,
  Image
} from 'react-native';

const API_URL = 'http://localhost:8000';

// ==================== SCREENS ====================

// Home Screen - Choose Level
const HomeScreen = ({ navigation }) => {
  const [levels, setLevels] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/levels`)
      .then(res => res.json())
      .then(data => setLevels(data))
      .catch(err => console.log(err));
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>📚 English File</Text>
        <Text style={styles.headerSubtitle}>Learn English through English!</Text>
      </View>
      <FlatList
        data={levels}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity 
            style={[styles.levelCard, { borderLeftColor: item.color }]}
            onPress={() => navigation.navigate('Lessons', { levelId: item.id })}
          >
            <Text style={styles.levelNumber}>Book {Math.ceil(item.id/2)}</Text>
            <Text style={styles.levelName}>{item.title}</Text>
            <Text style={styles.levelCefr}>{item.cefr}</Text>
            <Text style={styles.levelDesc}>{item.description}</Text>
          </TouchableOpacity>
        )}
        contentContainerStyle={styles.list}
      />
    </SafeAreaView>
  );
};

// Lessons Screen - Choose Module
const LessonsScreen = ({ route, navigation }) => {
  const { levelId } = route.params;
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/levels/${levelId}/lessons`)
      .then(res => res.json())
      .then(data => setLessons(data))
      .catch(err => console.log(err));
  }, [levelId]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backButton}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Module {levelId}</Text>
      </View>
      <FlatList
        data={lessons}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity 
            style={styles.lessonCard}
            onPress={() => navigation.navigate('Lesson', { lessonId: item.id })}
          >
            <View style={styles.lessonHeader}>
              <Text style={styles.lessonModule}>Module {item.module}</Text>
              <Text style={styles.lessonTopic}>{item.topic}</Text>
            </View>
            <Text style={styles.lessonTitle}>{item.title}</Text>
          </TouchableOpacity>
        )}
        contentContainerStyle={styles.list}
      />
    </SafeAreaView>
  );
};

// Lesson Detail Screen - 4 Parts
const LessonDetailScreen = ({ route, navigation }) => {
  const { lessonId } = route.params;
  const [lesson, setLesson] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/lessons/${lessonId}`)
      .then(res => res.json())
      .then(data => setLesson(data))
      .catch(err => console.log(err));
  }, [lessonId]);

  if (!lesson) return <View style={styles.container}><Text>Loading...</Text></View>;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backButton}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{lesson.title}</Text>
      </View>
      <ScrollView>
        {/* A. VOCABULARY - Pictures + Words */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>📷 A. Vocabulary</Text>
          <Text style={styles.sectionSubtitle}>Learn with pictures!</Text>
          <View style={styles.vocabGrid}>
            {lesson.vocabulary?.map((word, i) => (
              <View key={i} style={styles.vocabCard}>
                <View style={styles.vocabImage}>
                  <Text style={styles.vocabEmoji}>🖼️</Text>
                </View>
                <Text style={styles.vocabWord}>{word.word}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* B. GRAMMAR - In Context */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>📝 B. Grammar</Text>
          <Text style={styles.sectionSubtitle}>Look at the pattern!</Text>
          <View style={styles.grammarBox}>
            <Text style={styles.grammarPattern}>{lesson.grammar?.pattern}</Text>
            {lesson.grammar?.examples?.map((ex, i) => (
              <Text key={i} style={styles.grammarExample}>• {ex}</Text>
            ))}
          </View>
        </View>

        {/* C. EXERCISES */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>✏️ C. Practice</Text>
          <View style={styles.exercisesList}>
            {lesson.exercises?.map((ex, i) => (
              <TouchableOpacity key={i} style={styles.exerciseCard}>
                <Text style={styles.exerciseType}>{ex.type}</Text>
                <Text style={styles.exerciseText}>{ex.instruction}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* D. SPEAKING */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🗣️ D. Speaking</Text>
          <View style={styles.speakingBox}>
            <Text style={styles.speakingTask}>{lesson.speaking?.task}</Text>
            <Text style={styles.speakingPhrases}>
              Useful phrases: {lesson.speaking?.phrases?.join(', ')}
            </Text>
          </View>
          <TouchableOpacity 
            style={styles.speakButton}
            onPress={() => navigation.navigate('AI Tutor', { topic: lesson.topic })}
          >
            <Text style={styles.speakButtonText}>🎤 Practice with AI Tutor</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

// AI Tutor Screen
const AITutorScreen = ({ route }) => {
  const { topic } = route.params || {};
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([
    { role: 'ai', text: `Hi! Let's practice "${topic || 'English'}"! Speak in English - don't worry about mistakes!` }
  ]);

  const sendMessage = () => {
    if (!message.trim()) return;
    
    const userMsg = { role: 'user', text: message };
    setChat([...chat, userMsg]);
    
    // Call AI - responds in English only!
    fetch(`${API_URL}/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, user_id: 'demo' })
    })
    .then(res => res.json())
    .then(data => {
      setChat([...chat, userMsg, { role: 'ai', text: data.response }]);
    });
    
    setMessage('');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🎤 AI Tutor</Text>
        <Text style={styles.headerSubtitle}>Speak English only!</Text>
      </View>
      <FlatList
        data={chat}
        keyExtractor={(item, i) => i.toString()}
        renderItem={({ item }) => (
          <View style={[
            styles.chatMessage,
            item.role === 'user' ? styles.userMessage : styles.aiMessage
          ]}>
            <Text style={item.role === 'user' ? styles.userText : styles.aiText}>
              {item.text}
            </Text>
          </View>
        )}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={message}
          onChangeText={setMessage}
          placeholder="Type in English..."
          placeholderTextColor="#999"
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

// ==================== STYLES ====================

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { padding: 20, backgroundColor: '#4A90E2' },
  headerTitle: { fontSize: 24, fontWeight: 'bold', color: '#fff' },
  headerSubtitle: { fontSize: 14, color: '#ddd' },
  backButton: { fontSize: 16, color: '#fff', marginBottom: 10 },
  list: { padding: 16 },
  
  // Level Card
  levelCard: {
    backgroundColor: '#fff', borderRadius: 12, padding: 20, 
    marginBottom: 16, borderLeftWidth: 4, shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4
  },
  levelNumber: { fontSize: 14, color: '#888' },
  levelName: { fontSize: 22, fontWeight: 'bold', marginVertical: 4 },
  levelCefr: { fontSize: 18, color: '#4A90E2', fontWeight: '600' },
  levelDesc: { fontSize: 14, color: '#666', marginTop: 8 },
  
  // Lesson Card
  lessonCard: { backgroundColor: '#fff', borderRadius: 8, padding: 16, marginBottom: 12 },
  lessonHeader: { flexDirection: 'row', justifyContent: 'space-between' },
  lessonModule: { fontSize: 12, color: '#888', backgroundColor: '#eee', padding: 4, borderRadius: 4 },
  lessonTopic: { fontSize: 12, color: '#4A90E2' },
  lessonTitle: { fontSize: 18, fontWeight: '600', marginTop: 8 },
  
  // Sections
  section: { backgroundColor: '#fff', margin: 16, borderRadius: 12, padding: 16 },
  sectionTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 4 },
  sectionSubtitle: { fontSize: 14, color: '#888', marginBottom: 16 },
  
  // Vocabulary
  vocabGrid: { flexDirection: 'row', flexWrap: 'wrap' },
  vocabCard: { width: '45%', margin: '2.5%', alignItems: 'center' },
  vocabImage: { width: 80, height: 80, backgroundColor: '#eee', borderRadius: 8, justifyContent: 'center', alignItems: 'center' },
  vocabEmoji: { fontSize: 32 },
  vocabWord: { fontSize: 16, fontWeight: '600', marginTop: 8, textAlign: 'center' },
  
  // Grammar
  grammarBox: { backgroundColor: '#e3f2fd', padding: 16, borderRadius: 8 },
  grammarPattern: { fontSize: 18, fontWeight: 'bold', color: '#1565c0', marginBottom: 8 },
  grammarExample: { fontSize: 16, color: '#333', marginVertical: 4 },
  
  // Exercises
  exercisesList: {},
  exerciseCard: { backgroundColor: '#f5f5f5', padding: 16, borderRadius: 8, marginBottom: 8 },
  exerciseType: { fontSize: 12, color: '#888', textTransform: 'uppercase' },
  exerciseText: { fontSize: 16, fontWeight: '600', marginTop: 4 },
  
  // Speaking
  speakingBox: { backgroundColor: '#fff3e0', padding: 16, borderRadius: 8 },
  speakingTask: { fontSize: 18, fontWeight: 'bold', color: '#e65100', marginBottom: 8 },
  speakingPhrases: { fontSize: 14, color: '#666' },
  speakButton: { backgroundColor: '#4A90E2', padding: 16, borderRadius: 8, marginTop: 16, alignItems: 'center' },
  speakButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  
  // Chat
  chatMessage: { padding: 12, margin: 8, borderRadius: 12, maxWidth: '80%' },
  userMessage: { backgroundColor: '#4A90E2', alignSelf: 'flex-end' },
  aiMessage: { backgroundColor: '#fff', alignSelf: 'flex-start' },
  userText: { color: '#fff', fontSize: 16 },
  aiText: { color: '#333', fontSize: 16 },
  inputContainer: { flexDirection: 'row', padding: 10, backgroundColor: '#fff' },
  input: { flex: 1, borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 10 },
  sendButton: { backgroundColor: '#4A90E2', padding: 12, borderRadius: 8, marginLeft: 8 },
  sendButtonText: { color: '#fff', fontWeight: 'bold' },
});

export default App;
