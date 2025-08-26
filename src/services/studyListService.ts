import { supabase } from './supabase'
import { StudyList, StarredItem, StudyListItem, CustomFlashcard } from '../types/database.types'

export class StudyListService {
  // Helper to get the auto-generated study list name for a given item type
  private getAutoListName(itemType: StarredItem['item_type']): string {
    const listNames: Record<string, string> = {
      'spelling_word': 'Starred Spelling Words',
      'vocabulary_word': 'Starred Vocabulary Words',
      'language_question': 'Starred Language Questions',
      'question': 'Starred Questions',
      'skill_node': 'Starred Skills',
      'custom_question': 'Custom Questions'
    }
    return listNames[itemType] || 'Starred Items'
  }

  // Helper to get or create the auto-generated study list for starred items
  private async getOrCreateAutoList(
    userId: string, 
    itemType: StarredItem['item_type']
  ): Promise<StudyList | null> {
    try {
      const listName = this.getAutoListName(itemType)
      
      // Check if the list already exists
      const { data: existingList, error: fetchError } = await supabase
        .from('study_lists')
        .select('*')
        .eq('user_id', userId)
        .eq('name', listName)
        .single()
      
      if (existingList && !fetchError) {
        return existingList
      }
      
      // Create the list if it doesn't exist
      const listColors: Record<string, string> = {
        'spelling_word': '#8B5CF6', // Purple
        'vocabulary_word': '#10B981', // Green
        'language_question': '#F59E0B', // Amber
        'question': '#3B82F6', // Blue
        'skill_node': '#EF4444', // Red
        'custom_question': '#06B6D4' // Cyan
      }
      
      const { data: newList, error: createError } = await supabase
        .from('study_lists')
        .insert({
          user_id: userId,
          name: listName,
          description: '',
          color: listColors[itemType] || '#6B7280',
          is_public: false
        })
        .select()
        .single()
      
      if (createError) {
        console.error('Error creating auto study list:', createError)
        return null
      }
      
      return newList
    } catch (error) {
      console.error('Error getting/creating auto study list:', error)
      return null
    }
  }

  // Starred Items Management
  async starItem(
    userId: string, 
    itemType: StarredItem['item_type'], 
    itemId: string, 
    itemData?: any
  ): Promise<boolean> {
    try {
      // First, add to starred items
      const { error: starError } = await supabase
        .from('starred_items')
        .insert({
          user_id: userId,
          item_type: itemType,
          item_id: itemId,
          item_data: itemData
        })

      if (starError) {
        console.error('Error starring item:', starError)
        return false
      }

      // Then, add to the auto-generated study list
      const autoList = await this.getOrCreateAutoList(userId, itemType)
      if (autoList) {
        // Check if item is already in the list
        const { data: existingItem } = await supabase
          .from('study_list_items')
          .select('id')
          .eq('study_list_id', autoList.id)
          .eq('item_type', itemType)
          .eq('item_id', itemId)
          .single()
        
        // Only add if not already in the list
        if (!existingItem) {
          await supabase
            .from('study_list_items')
            .insert({
              study_list_id: autoList.id,
              item_type: itemType,
              item_id: itemId,
              item_data: itemData,
              notes: 'Auto-added from starred items'
            })
        }
      }

      return true
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
      // First, remove from starred items
      const { error: unstarError } = await supabase
        .from('starred_items')
        .delete()
        .eq('user_id', userId)
        .eq('item_type', itemType)
        .eq('item_id', itemId)

      if (unstarError) {
        console.error('Error unstarring item:', unstarError)
        return false
      }

      // Then, remove from the auto-generated study list
      const listName = this.getAutoListName(itemType)
      
      // Get the auto-generated list
      const { data: autoList } = await supabase
        .from('study_lists')
        .select('id')
        .eq('user_id', userId)
        .eq('name', listName)
        .single()
      
      if (autoList) {
        // Remove from the auto-generated study list
        await supabase
          .from('study_list_items')
          .delete()
          .eq('study_list_id', autoList.id)
          .eq('item_type', itemType)
          .eq('item_id', itemId)
      }

      return true
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
        .limit(1)

      return !error && data && data.length > 0
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

  // Migrate existing starred items to auto-generated study lists
  async migrateStarredItemsToLists(userId: string): Promise<void> {
    try {
      // Get all starred items for the user
      const { data: starredItems, error } = await supabase
        .from('starred_items')
        .select('*')
        .eq('user_id', userId)
      
      if (error || !starredItems) {
        console.error('Error fetching starred items for migration:', error)
        return
      }

      // Group items by type
      const itemsByType = starredItems.reduce((acc, item) => {
        if (!acc[item.item_type]) {
          acc[item.item_type] = []
        }
        acc[item.item_type].push(item)
        return acc
      }, {} as Record<string, StarredItem[]>)

      // Process each type
      for (const [itemType, items] of Object.entries(itemsByType)) {
        const autoList = await this.getOrCreateAutoList(userId, itemType as StarredItem['item_type'])
        
        if (autoList) {
          // Get existing items in the list to avoid duplicates
          const { data: existingItems } = await supabase
            .from('study_list_items')
            .select('item_id')
            .eq('study_list_id', autoList.id)
            .eq('item_type', itemType)
          
          const existingItemIds = new Set(existingItems?.map(item => item.item_id) || [])
          
          // Add items that aren't already in the list
          const typedItems = items as StarredItem[]
          const itemsToAdd = typedItems
            .filter((item) => !existingItemIds.has(item.item_id))
            .map((item) => ({
              study_list_id: autoList.id,
              item_type: item.item_type,
              item_id: item.item_id,
              item_data: item.item_data,
              notes: 'Migrated from starred items'
            }))
          
          if (itemsToAdd.length > 0) {
            const { error: insertError } = await supabase
              .from('study_list_items')
              .insert(itemsToAdd)
            
            if (insertError) {
              console.error(`Error migrating ${itemType} items:`, insertError)
            } else {
              console.log(`Migrated ${itemsToAdd.length} ${itemType} items to study list`)
            }
          }
        }
      }
    } catch (error) {
      console.error('Error migrating starred items:', error)
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
        .limit(1)

      return !error && data && data.length > 0
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