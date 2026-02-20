import { create } from 'zustand'

interface CostStore {
  totalCost: number
  totalTokens: number
  totalCalls: number
  costByModel: Record<string, number>
  updateCost: (cost: number, tokens: number, model: string) => void
  reset: () => void
}

export const useCostStore = create<CostStore>((set) => ({
  totalCost: 0,
  totalTokens: 0,
  totalCalls: 0,
  costByModel: {},
  updateCost: (cost, tokens, model) =>
    set((state) => ({
      totalCost: state.totalCost + cost,
      totalTokens: state.totalTokens + tokens,
      totalCalls: state.totalCalls + 1,
      costByModel: {
        ...state.costByModel,
        [model]: (state.costByModel[model] || 0) + cost,
      },
    })),
  reset: () =>
    set({
      totalCost: 0,
      totalTokens: 0,
      totalCalls: 0,
      costByModel: {},
    }),
}))
