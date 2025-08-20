import { supabase } from './supabase'
import { StudyList, StarredItem, StudyListItem, CustomFlashcard } from '../types/database.types'

export class StudyListService {
  // Starred Items Management
  async starItem(
    userId: string, 
    itemType: StarredItem['item_type'], 
    itemId: string, 
    itemData?: any
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('starred_items')
        .insert({
          user_id: userId,
          item_type: itemType,
          item_id: itemId,
          item_data: itemData
        })

      return !error
    } catch (error) {
      console.error('Error starring item:', error)
      return false
    }
  }

  async unstarItem(
    userId: string, 
    itemType: StarredItem['item_type'], 
    itemId: string
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('starred_items')
        .delete()
        .eq('user_id', userId)
        .eq('item_type', itemType)
        .eq('item_id', itemId)

      return !error
    } catch (error) {
      console.error('Error unstarring item:', error)
      return false
    }
  }

  async isItemStarred(
    userId: string, 
    itemType: StarredItem['item_type'], 
    itemId: string
  ): Promise<boolean> {
    try {
      const { data, error } = await supabase
        .from('starred_items')
        .select('id')
        .eq('user_id', userId)
        .eq('item_type', itemType)
        .eq('item_id', itemId)
        .single()

      return !error && !!data
    } catch (error) {
      return false
    }
  }

  async getStarredItems(userId: string, itemType?: StarredItem['item_type']): Promise<StarredItem[]> {
    try {
      let query = supabase
        .from('starred_items')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })

      if (itemType) {
        query = query.eq('item_type', itemType)
      }

      const { data, error } = await query

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching starred items:', error)
      return []
    }
  }

  // Study Lists Management
  async createStudyList(
    userId: string, 
    name: string, 
    description?: string, 
    color?: string,
    isPublic?: boolean
  ): Promise<StudyList | null> {
    try {
      const { data, error } = await supabase
        .from('study_lists')
        .insert({
          user_id: userId,
          name,
          description,
          color: color || '#3B82F6',
          is_public: isPublic || false
        })
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error creating study list:', error)
      return null
    }
  }

  async getUserStudyLists(userId: string): Promise<StudyList[]> {
    try {
      const { data, error } = await supabase
        .from('study_lists')
        .select('*')
        .eq('user_id', userId)
        .order('updated_at', { ascending: false })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching study lists:', error)
      return []
    }
  }

  async updateStudyList(
    studyListId: string, 
    updates: Partial<Pick<StudyList, 'name' | 'description' | 'color' | 'is_public'>>
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_lists')
        .update({ ...updates, updated_at: new Date().toISOString() })
        .eq('id', studyListId)

      return !error
    } catch (error) {
      console.error('Error updating study list:', error)
      return false
    }
  }

  async deleteStudyList(studyListId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_lists')
        .delete()
        .eq('id', studyListId)

      return !error
    } catch (error) {
      console.error('Error deleting study list:', error)
      return false
    }
  }

  // Study List Items Management
  async addItemToStudyList(
    studyListId: string,
    itemType: StudyListItem['item_type'],
    itemId: string,
    itemData?: any,
    notes?: string
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_list_items')
        .insert({
          study_list_id: studyListId,
          item_type: itemType,
          item_id: itemId,
          item_data: itemData,
          notes
        })

      return !error
    } catch (error) {
      console.error('Error adding item to study list:', error)
      return false
    }
  }

  async removeItemFromStudyList(
    studyListId: string,
    itemType: StudyListItem['item_type'],
    itemId: string
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_list_items')
        .delete()
        .eq('study_list_id', studyListId)
        .eq('item_type', itemType)
        .eq('item_id', itemId)

      return !error
    } catch (error) {
      console.error('Error removing item from study list:', error)
      return false
    }
  }

  async getStudyListItems(studyListId: string): Promise<StudyListItem[]> {
    try {
      const { data, error } = await supabase
        .from('study_list_items')
        .select('*')
        .eq('study_list_id', studyListId)
        .order('added_at', { ascending: false })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching study list items:', error)
      return []
    }
  }

  async isItemInStudyList(
    studyListId: string,
    itemType: StudyListItem['item_type'],
    itemId: string
  ): Promise<boolean> {
    try {
      const { data, error } = await supabase
        .from('study_list_items')
        .select('id')
        .eq('study_list_id', studyListId)
        .eq('item_type', itemType)
        .eq('item_id', itemId)
        .single()

      return !error && !!data
    } catch (error) {
      return false
    }
  }

  // Custom Flashcards Management
  async createCustomFlashcard(
    userId: string,
    front: string,
    back: string,
    category?: string,
    tags?: string[],
    difficultyLevel?: number
  ): Promise<CustomFlashcard | null> {
    try {
      const { data, error } = await supabase
        .from('custom_flashcards')
        .insert({
          user_id: userId,
          front,
          back,
          category,
          tags,
          difficulty_level: difficultyLevel
        })
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error creating custom flashcard:', error)
      return null
    }
  }

  async getUserCustomFlashcards(userId: string, category?: string): Promise<CustomFlashcard[]> {
    try {
      let query = supabase
        .from('custom_flashcards')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })

      if (category) {
        query = query.eq('category', category)
      }

      const { data, error } = await query

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching custom flashcards:', error)
      return []
    }
  }

  async updateCustomFlashcard(
    flashcardId: string,
    updates: Partial<Pick<CustomFlashcard, 'front' | 'back' | 'category' | 'tags' | 'difficulty_level'>>
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('custom_flashcards')
        .update({ ...updates, updated_at: new Date().toISOString() })
        .eq('id', flashcardId)

      return !error
    } catch (error) {
      console.error('Error updating custom flashcard:', error)
      return false
    }
  }

  async deleteCustomFlashcard(flashcardId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('custom_flashcards')
        .delete()
        .eq('id', flashcardId)

      return !error
    } catch (error) {
      console.error('Error deleting custom flashcard:', error)
      return false
    }
  }

  // Study Sessions
  async startStudySession(userId: string, studyListId: string): Promise<string | null> {
    try {
      const { data, error } = await supabase
        .from('study_sessions')
        .insert({
          user_id: userId,
          study_list_id: studyListId
        })
        .select('id')
        .single()

      if (error) throw error
      return data.id
    } catch (error) {
      console.error('Error starting study session:', error)
      return null
    }
  }

  async endStudySession(
    sessionId: string,
    itemsStudied: number,
    itemsCorrect: number,
    totalTimeSeconds: number
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_sessions')
        .update({
          ended_at: new Date().toISOString(),
          items_studied: itemsStudied,
          items_correct: itemsCorrect,
          total_time_seconds: totalTimeSeconds
        })
        .eq('id', sessionId)

      return !error
    } catch (error) {
      console.error('Error ending study session:', error)
      return false
    }
  }
}

export const studyListService = new StudyListService()