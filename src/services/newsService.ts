import { supabase } from './supabase'

export interface NewsItem {
  id: string
  title: string
  description: string
  icon_name?: string
  link?: string
  link_text?: string
  date_posted: string
  is_published: boolean
  display_order: number
  created_at: string
  updated_at: string
  created_by?: string
}

export const newsService = {
  async getPublishedNews(limit: number = 10): Promise<NewsItem[]> {
    try {
      const { data, error } = await supabase
        .from('news_items')
        .select('*')
        .eq('is_published', true)
        .order('display_order', { ascending: true })
        .order('date_posted', { ascending: false })
        .limit(limit)

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching news:', error)
      return []
    }
  },

  async getAllNews(): Promise<NewsItem[]> {
    try {
      const { data, error } = await supabase
        .from('news_items')
        .select('*')
        .order('display_order', { ascending: true })
        .order('date_posted', { ascending: false })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching all news:', error)
      return []
    }
  },

  async createNewsItem(item: Omit<NewsItem, 'id' | 'created_at' | 'updated_at'>): Promise<NewsItem | null> {
    try {
      const { data: userData } = await (supabase.auth as any).getSession()
      const { data, error } = await supabase
        .from('news_items')
        .insert({
          ...item,
          created_by: userData?.session?.user?.id
        })
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error creating news item:', error)
      return null
    }
  },

  async updateNewsItem(id: string, updates: Partial<NewsItem>): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('news_items')
        .update(updates)
        .eq('id', id)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error updating news item:', error)
      return false
    }
  },

  async deleteNewsItem(id: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('news_items')
        .delete()
        .eq('id', id)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error deleting news item:', error)
      return false
    }
  },

  async togglePublished(id: string, isPublished: boolean): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('news_items')
        .update({ is_published: isPublished })
        .eq('id', id)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error toggling news published status:', error)
      return false
    }
  }
}